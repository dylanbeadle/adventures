// Makes a hero's published model: one animation clip (Idle by default), Y-up metres, textures
// compressed (AVIF at standard quality), the same bytes every run.
//
//   xcrun swift scripts/make-hero-model.swift <source.usdz> <out.usdz> [clip]
//
// The source is a hero master as 3DAssets delivered it (`heroes/<role>/minimal/<role>_minimal.usdz`:
// Z-up metres, five SkelAnimation clips chosen by a `clip` variant set). The table plays whatever
// clips a model has, so an idle-only hero idles everywhere (Spatial GM D147; Plan 2.0g).
import Foundation
import System
import USDKit

let args = CommandLine.arguments
guard args.count >= 3 else {
    FileHandle.standardError.write(Data("usage: make-hero-model.swift <source.usdz> <out.usdz> [clip]\n".utf8))
    exit(2)
}
let source = URL(fileURLWithPath: args[1])
let output = URL(fileURLWithPath: args[2])
let keep = args.count > 3 ? args[3] : "Idle"
let fm = FileManager.default

func run(_ tool: String, _ arguments: [String]) throws {
    let process = Process()
    process.executableURL = URL(fileURLWithPath: tool)
    process.arguments = arguments
    try process.run()
    process.waitUntilExit()
    guard process.terminationStatus == 0 else { throw CocoaError(.fileReadCorruptFile) }
}

let work = fm.temporaryDirectory.appendingPathComponent("HeroModel-\(UUID().uuidString)", isDirectory: true)
try fm.createDirectory(at: work.appendingPathComponent("textures"), withIntermediateDirectories: true)
defer { try? fm.removeItem(at: work) }   // try?: a temporary folder

// 1. Unpacked, so its textures are files (inside a package they're `x.usdz[0/a.png]` paths).
let unpacked = work.appendingPathComponent("source", isDirectory: true)
try run("/usr/bin/unzip", ["-q", source.path, "-d", unpacked.path])
guard let rootName = try fm.contentsOfDirectory(atPath: unpacked.path).first(where: { $0.hasSuffix(".usdc") || $0.hasSuffix(".usda") }) else {
    throw CocoaError(.fileReadCorruptFile)
}
let root = unpacked.appendingPathComponent(rootName)
let sourceStage = try USDStage.open(rootLayer: try USDLayer.open(root.path))
guard let prim = sourceStage.rootLayer.defaultPrim.map({ "\($0)" }) else { throw CocoaError(.fileReadCorruptFile) }
let zUp = "\(sourceStage.upAxis)".uppercased() == "Z"
let metres = sourceStage.metersPerUnit > 0 ? sourceStage.metersPerUnit : 1
// The clips' timing, which flattening a wrapper would otherwise lose (the source plays at 30 per second).
let timing = work.appendingPathComponent("timing.usda")
try sourceStage.rootLayer.export(to: timing)
let header = (try String(contentsOf: timing, encoding: .utf8)).components(separatedBy: "\n").prefix(40).joined(separator: "\n")
func metadata(_ key: String) -> String? {
    header.range(of: "\(key) = ([0-9.]+)", options: .regularExpression).map { String(header[$0]).components(separatedBy: " = ")[1] }
}

// 2. A wrapper: Y-up metres, the one clip selected, referencing the source.
let wrapper = work.appendingPathComponent("wrapper.usda")
try """
#usda 1.0
(
    defaultPrim = "\(prim)"
    metersPerUnit = 1
    upAxis = "Y"
    timeCodesPerSecond = \(metadata("timeCodesPerSecond") ?? "24")
    startTimeCode = \(metadata("startTimeCode") ?? "0")
    endTimeCode = \(metadata("endTimeCode") ?? "0")
)

def "\(prim)" (
    kind = "component"
    prepend references = @\(root.path)@
    variants = {
        string clip = "\(keep)"
    }
)
{
    float xformOp:rotateX = \(zUp ? -90 : 0)
    double3 xformOp:scale = (\(metres), \(metres), \(metres))
    uniform token[] xformOpOrder = ["xformOp:rotateX", "xformOp:scale"]
}

""".write(to: wrapper, atomically: true, encoding: .utf8)

// 3. Flattened (the clip's variant baked in), the other clips removed.
let flat = work.appendingPathComponent("flat.usda")
try USDStage.open(rootLayer: try USDLayer.open(wrapper.path)).exportFlattened(to: flat)
let flatStage = try USDStage.open(rootLayer: try USDLayer.open(flat.path))
var removed: [String] = []
for p in flatStage.allDescendants {
    let spec = flatStage.rootLayer.prim(at: p.path)
    if spec.map({ "\($0.typeName)" == "SkelAnimation" }) == true, "\(p.path.description)".split(separator: "/").last.map(String.init) != keep {
        removed.append(p.path.description)
    }
}
for path in removed { _ = flatStage.removePrim(at: USDLayer.Path(stringLiteral: path)) }
let model = work.appendingPathComponent("model.usda")
try flatStage.rootLayer.export(to: model)

// 4. Textures beside the layer, by name (flattening made their paths absolute), then binary and packaged.
var text = try String(contentsOf: model, encoding: .utf8)
var copied: [String: String] = [:]
for path in Set(text.matches(of: /@([^@\n]+)@/).map { String($0.output.1) }).sorted() where path.hasPrefix("/") {
    let file = URL(fileURLWithPath: path)
    guard fm.fileExists(atPath: file.path) else { continue }
    var name = file.lastPathComponent
    var n = 2
    while copied.values.contains("textures/\(name)") { name = "\(n)-\(file.lastPathComponent)"; n += 1 }
    try fm.copyItem(at: file, to: work.appendingPathComponent("textures/\(name)"))
    copied[path] = "textures/\(name)"
}
for (path, local) in copied { text = text.replacingOccurrences(of: "@\(path)@", with: "@\(local)@") }
text = text.replacingOccurrences(of: work.path, with: ".")
try text.write(to: model, atomically: true, encoding: .utf8)
let binary = work.appendingPathComponent("model.usdc")
try USDLayer.open(model.path).export(to: binary)
let stage = try USDStage.open(rootLayer: try USDLayer.open(binary.path))
let data = try stage.exportPackage(options: [.preferSmallTextureFiles(quality: .standard)])

// Fixed zip dates: the same source makes the same bytes.
var bytes = [UInt8](data)
func u16(_ i: Int) -> Int { i + 1 < bytes.count ? Int(bytes[i]) | Int(bytes[i + 1]) << 8 : 0 }
func u32(_ i: Int) -> Int { i + 3 < bytes.count ? u16(i) | u16(i + 2) << 16 : 0 }
let date = (2026 - 1980) << 9 | 1 << 5 | 1
func stamp(_ at: Int) { bytes[at] = 0; bytes[at + 1] = 0; bytes[at + 2] = UInt8(date & 0xFF); bytes[at + 3] = UInt8(date >> 8) }
var eocd = bytes.count - 22
while eocd > 0, u32(eocd) != 0x0605_4b50 { eocd -= 1 }
var cursor = u32(eocd + 16)
for _ in 0..<u16(eocd + 10) {
    stamp(cursor + 12)
    let local = u32(cursor + 42)
    if u32(local) == 0x0403_4b50 { stamp(local + 10) }
    cursor += 46 + u16(cursor + 28) + u16(cursor + 30) + u16(cursor + 32)
}
try Data(bytes).write(to: output)
print("\(output.lastPathComponent): \(bytes.count / 1000) KB, kept \(keep), removed \(removed.count) clips (\(removed.map { $0.split(separator: "/").last.map(String.init) ?? $0 }.joined(separator: ", ")))")
