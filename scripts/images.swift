// Catalogue images, with ImageIO (no third-party tools; runs on any Mac and the macOS Action runner).
//
//   swiftc -O scripts/images.swift -o <tool>
//   <tool> thumbs <size> <out folder> <in.png>...        each image, fitted in a square on the backdrop, as <name>.jpg
//   <tool> cover <size> <out.jpg> <in>...                 the images in a square grid (3 × 3 for 9) on the backdrop
//   <tool> fit <size> <out.jpg> <in>                      one image scaled to fit, for the site's cover list
//
// The backdrop is a neutral dark grey, so a transparent render reads in light and dark pages alike.
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let backdrop = CGColor(srgbRed: 0.17, green: 0.18, blue: 0.2, alpha: 1)

func load(_ path: String) -> CGImage? {
    guard let source = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil) else { return nil }
    return CGImageSourceCreateImageAtIndex(source, 0, nil)
}

func canvas(_ width: Int, _ height: Int) -> CGContext {
    let context = CGContext(data: nil, width: width, height: height, bitsPerComponent: 8, bytesPerRow: 0,
                            space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    context.interpolationQuality = .high
    context.setFillColor(backdrop)
    context.fill(CGRect(x: 0, y: 0, width: width, height: height))
    return context
}

func draw(_ image: CGImage, in rect: CGRect, on context: CGContext) {
    let scale = min(rect.width / CGFloat(image.width), rect.height / CGFloat(image.height))
    let size = CGSize(width: CGFloat(image.width) * scale, height: CGFloat(image.height) * scale)
    context.draw(image, in: CGRect(x: rect.midX - size.width / 2, y: rect.midY - size.height / 2, width: size.width, height: size.height))
}

func save(_ context: CGContext, to path: String, quality: Double = 0.78) {
    let url = URL(fileURLWithPath: path)
    try? FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)   // try?: the write below reports
    guard let image = context.makeImage(),
          let destination = CGImageDestinationCreateWithURL(url as CFURL, UTType.jpeg.identifier as CFString, 1, nil) else {
        FileHandle.standardError.write(Data("can't write \(path)\n".utf8)); exit(1)
    }
    CGImageDestinationAddImage(destination, image, [kCGImageDestinationLossyCompressionQuality: quality] as CFDictionary)
    guard CGImageDestinationFinalize(destination) else { FileHandle.standardError.write(Data("can't write \(path)\n".utf8)); exit(1) }
}

let args = Array(CommandLine.arguments.dropFirst())
guard args.count >= 4, let size = Int(args[1]) else {
    FileHandle.standardError.write(Data("usage: images thumbs|cover|fit <size> <out> <in>...\n".utf8)); exit(2)
}
let inputs = Array(args[3...])
switch args[0] {
case "thumbs":
    for path in inputs {
        guard let image = load(path) else { FileHandle.standardError.write(Data("can't read \(path)\n".utf8)); continue }
        let context = canvas(size, size)
        draw(image, in: CGRect(x: 0, y: 0, width: size, height: size), on: context)
        let name = (URL(fileURLWithPath: path).deletingPathExtension().lastPathComponent)
        save(context, to: "\(args[2])/\(name).jpg")
    }
case "cover":
    let images = inputs.compactMap(load)
    let columns = max(1, Int(Double(images.count).squareRoot().rounded(.up)))
    let rows = max(1, (images.count + columns - 1) / columns)
    let cell = CGFloat(size) / CGFloat(columns)
    let context = canvas(size, size)
    let top = (CGFloat(size) - cell * CGFloat(rows)) / 2
    for (i, image) in images.enumerated() {
        let row = i / columns, column = i % columns
        let y = CGFloat(size) - top - cell * CGFloat(row + 1)
        draw(image, in: CGRect(x: cell * CGFloat(column), y: y, width: cell, height: cell), on: context)
    }
    save(context, to: args[2])
case "fit":
    guard let image = load(inputs[0]) else { FileHandle.standardError.write(Data("can't read \(inputs[0])\n".utf8)); exit(1) }
    let scale = min(1, CGFloat(size) / CGFloat(max(image.width, image.height)))
    let width = Int(CGFloat(image.width) * scale), height = Int(CGFloat(image.height) * scale)
    let context = canvas(width, height)
    draw(image, in: CGRect(x: 0, y: 0, width: width, height: height), on: context)
    save(context, to: args[2], quality: 0.82)
default:
    FileHandle.standardError.write(Data("unknown command \(args[0])\n".utf8)); exit(2)
}
