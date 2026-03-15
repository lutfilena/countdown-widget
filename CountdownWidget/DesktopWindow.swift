import AppKit
import SwiftUI

protocol DesktopWindowContextMenuDelegate: AnyObject {
    func contextMenuItems() -> [NSMenuItem]
}

class DesktopWindow: NSWindow {
    private weak var contextMenuDelegate: DesktopWindowContextMenuDelegate?

    init<Content: View>(contentView: Content) {
        super.init(
            contentRect: NSRect(x: 0, y: 0, width: 420, height: 500),
            styleMask: [.borderless],
            backing: .buffered,
            defer: false
        )

        // Use normal level so it receives all mouse events
        // But keep it behind most windows
        self.level = .normal
        self.collectionBehavior = [.canJoinAllSpaces, .managed, .fullScreenAuxiliary]
        self.isOpaque = false
        self.backgroundColor = .clear
        self.hasShadow = true
        self.ignoresMouseEvents = false
        self.isMovableByWindowBackground = true  // Simple click+drag anywhere
        self.isReleasedWhenClosed = false

        let hostView = NSHostingView(rootView: contentView)
        hostView.frame = self.frame

        // Add vibrancy background
        let visualEffect = NSVisualEffectView(frame: self.frame)
        visualEffect.material = .hudWindow
        visualEffect.blendingMode = .behindWindow
        visualEffect.state = .active
        visualEffect.wantsLayer = true
        visualEffect.layer?.cornerRadius = 16
        visualEffect.layer?.masksToBounds = true
        visualEffect.autoresizingMask = [.width, .height]

        hostView.autoresizingMask = [.width, .height]
        visualEffect.addSubview(hostView)

        self.contentView = visualEffect

        // Position in bottom-right area of screen
        if let screen = NSScreen.main {
            let screenFrame = screen.visibleFrame
            let x = screenFrame.maxX - self.frame.width - 40
            let y = screenFrame.minY + 40
            self.setFrameOrigin(NSPoint(x: x, y: y))
        }

        self.orderFront(nil)
    }

    func makeContextMenu(delegate: DesktopWindowContextMenuDelegate) {
        self.contextMenuDelegate = delegate
    }

    override func rightMouseDown(with event: NSEvent) {
        guard let delegate = contextMenuDelegate else {
            super.rightMouseDown(with: event)
            return
        }
        let menu = NSMenu()
        for item in delegate.contextMenuItems() {
            menu.addItem(item)
        }
        NSMenu.popUpContextMenu(menu, with: event, for: self.contentView!)
    }

    override var canBecomeKey: Bool { true }
    override var canBecomeMain: Bool { false }
}
