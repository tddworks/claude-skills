#!/usr/bin/env python3
"""
Scaffold an iOS app with Tuist and layered architecture.
Usage: python3 scaffold.py <AppName> <output-directory> [--bundle-id <bundle-id>] [--team-id <team-id>]
"""

import argparse
import os
import sys

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"  Created: {path}")

def to_bundle_id(name):
    return name.lower().replace(' ', '').replace('-', '').replace('_', '')

def scaffold_app(app_name: str, output_dir: str, bundle_id: str = None, team_id: str = "YOUR_TEAM_ID"):
    """Scaffold a new iOS app with Tuist and layered architecture."""

    if bundle_id is None:
        bundle_id = f"com.example.{to_bundle_id(app_name)}"

    root = os.path.join(output_dir, app_name)

    print(f"\n🚀 Scaffolding {app_name} at {root}\n")

    # Create directory structure
    dirs = [
        f"{root}/Sources/App/Views",
        f"{root}/Sources/App/Resources/Assets.xcassets/AppIcon.appiconset",
        f"{root}/Sources/App/Resources/Assets.xcassets/AccentColor.colorset",
        f"{root}/Sources/App/Resources/XCConfig",
        f"{root}/Sources/App/Resources/en.lproj",
        f"{root}/Sources/App/Application",
        f"{root}/Sources/App/Extensions",
        f"{root}/Sources/Domain/Models",
        f"{root}/Sources/Domain/Protocols",
        f"{root}/Sources/Domain/Utils",
        f"{root}/Sources/Infrastructure/Local",
        f"{root}/Tests/DomainTests",
        f"{root}/Tests/InfrastructureTests",
        f"{root}/design-prototype",
    ]

    for d in dirs:
        create_directory(d)

    # Project.swift
    write_file(f"{root}/Project.swift", f'''import ProjectDescription

let project = Project(
    name: "{app_name}",
    options: .options(
        defaultKnownRegions: ["en"],
        developmentRegion: "en"
    ),
    packages: [
        .remote(url: "https://github.com/Kolos65/Mockable.git", requirement: .upToNextMajor(from: "0.5.0")),
    ],
    settings: .settings(
        base: [
            "SWIFT_VERSION": "6.0",
            "IPHONEOS_DEPLOYMENT_TARGET": "18.0",
            "ENABLE_DEBUG_DYLIB": "YES",
        ],
        debug: [
            "SWIFT_ACTIVE_COMPILATION_CONDITIONS": "DEBUG MOCKING",
            "ENABLE_DEBUG_DYLIB": "YES",
        ],
        release: [
            "SWIFT_ACTIVE_COMPILATION_CONDITIONS": "MOCKING",
        ]
    ),
    targets: [
        // MARK: - Domain Layer
        .target(
            name: "Domain",
            destinations: .iOS,
            product: .staticFramework,
            bundleId: "{bundle_id}.domain",
            deploymentTargets: .iOS("18.0"),
            sources: ["Sources/Domain/**"],
            dependencies: [
                .package(product: "Mockable"),
            ],
            settings: .settings(
                base: ["SWIFT_STRICT_CONCURRENCY": "complete"]
            )
        ),

        // MARK: - Infrastructure Layer
        .target(
            name: "Infrastructure",
            destinations: .iOS,
            product: .staticFramework,
            bundleId: "{bundle_id}.infrastructure",
            deploymentTargets: .iOS("18.0"),
            sources: ["Sources/Infrastructure/**"],
            dependencies: [
                .target(name: "Domain"),
                .package(product: "Mockable"),
            ],
            settings: .settings(
                base: ["SWIFT_STRICT_CONCURRENCY": "complete"]
            )
        ),

        // MARK: - Main Application
        .target(
            name: "{app_name}",
            destinations: .iOS,
            product: .app,
            bundleId: "{bundle_id}",
            deploymentTargets: .iOS("18.0"),
            infoPlist: .file(path: "Sources/App/Info.plist"),
            sources: ["Sources/App/**"],
            resources: ["Sources/App/Resources/**"],
            entitlements: .file(path: "Sources/App/{app_name}.entitlements"),
            dependencies: [
                .target(name: "Domain"),
                .target(name: "Infrastructure"),
            ],
            settings: .settings(
                base: [
                    "SWIFT_STRICT_CONCURRENCY": "complete",
                    "ENABLE_DEBUG_DYLIB": "YES",
                    "ENABLE_PREVIEWS": "YES",
                    "ASSETCATALOG_COMPILER_APPICON_NAME": "AppIcon",
                    "MARKETING_VERSION": "1.0.0",
                    "CURRENT_PROJECT_VERSION": "1",
                ],
                configurations: [
                    .debug(name: .debug, xcconfig: "Sources/App/Resources/XCConfig/debug.xcconfig"),
                    .release(name: .release, xcconfig: "Sources/App/Resources/XCConfig/release.xcconfig"),
                ],
                defaultSettings: .recommended(excluding: ["CODE_SIGN_IDENTITY"])
            )
        ),

        // MARK: - Domain Tests
        .target(
            name: "DomainTests",
            destinations: .iOS,
            product: .unitTests,
            bundleId: "{bundle_id}.domain-tests",
            deploymentTargets: .iOS("18.0"),
            sources: ["Tests/DomainTests/**"],
            dependencies: [
                .target(name: "Domain"),
                .package(product: "Mockable"),
            ],
            settings: .settings(
                base: ["SWIFT_ACTIVE_COMPILATION_CONDITIONS": "MOCKING"]
            )
        ),

        // MARK: - Infrastructure Tests
        .target(
            name: "InfrastructureTests",
            destinations: .iOS,
            product: .unitTests,
            bundleId: "{bundle_id}.infrastructure-tests",
            deploymentTargets: .iOS("18.0"),
            sources: ["Tests/InfrastructureTests/**"],
            dependencies: [
                .target(name: "Infrastructure"),
                .target(name: "Domain"),
                .package(product: "Mockable"),
            ],
            settings: .settings(
                base: ["SWIFT_ACTIVE_COMPILATION_CONDITIONS": "MOCKING"]
            )
        ),
    ],
    schemes: [
        .scheme(
            name: "{app_name}",
            shared: true,
            buildAction: .buildAction(targets: ["{app_name}"]),
            testAction: .targets(
                [
                    .testableTarget(target: .target("DomainTests")),
                    .testableTarget(target: .target("InfrastructureTests")),
                ],
                configuration: .debug
            ),
            runAction: .runAction(configuration: .debug, executable: .target("{app_name}")),
            archiveAction: .archiveAction(configuration: .release),
            profileAction: .profileAction(configuration: .release, executable: .target("{app_name}")),
            analyzeAction: .analyzeAction(configuration: .debug)
        ),
    ]
)
''')

    # Tuist.swift
    write_file(f"{root}/Tuist.swift", '''import ProjectDescription

let config = Config(
    compatibleXcodeVersions: .all,
    swiftVersion: "6.0"
)
''')

    # .gitignore
    write_file(f"{root}/.gitignore", '''# Xcode
*.xcodeproj
*.xcworkspace
xcuserdata/
DerivedData/
*.ipa
*.dSYM.zip
*.dSYM

# Tuist
Derived/

# Swift Package Manager
.build/
.swiftpm/

# macOS
.DS_Store

# IDE
.idea/

# Test Results
TestResults.xcresult
''')

    # Info.plist
    write_file(f"{root}/Sources/App/Info.plist", f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>$(DEVELOPMENT_LANGUAGE)</string>
    <key>CFBundleDisplayName</key>
    <string>{app_name}</string>
    <key>CFBundleExecutable</key>
    <string>$(EXECUTABLE_NAME)</string>
    <key>CFBundleIdentifier</key>
    <string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>$(PRODUCT_NAME)</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>$(MARKETING_VERSION)</string>
    <key>CFBundleVersion</key>
    <string>$(CURRENT_PROJECT_VERSION)</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>UIApplicationSceneManifest</key>
    <dict>
        <key>UIApplicationSupportsMultipleScenes</key>
        <true/>
    </dict>
    <key>UILaunchScreen</key>
    <dict>
        <key>UIColorName</key>
        <string>AccentColor</string>
    </dict>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>arm64</string>
    </array>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
    </array>
</dict>
</plist>
''')

    # Entitlements
    write_file(f"{root}/Sources/App/{app_name}.entitlements", '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
</dict>
</plist>
''')

    # App entry point
    write_file(f"{root}/Sources/App/{app_name}App.swift", f'''import SwiftUI
import Domain
import Infrastructure

@main
struct {app_name}App: App {{
    var body: some Scene {{
        WindowGroup {{
            ContentView()
        }}
    }}
}}
''')

    # ContentView
    write_file(f"{root}/Sources/App/Views/ContentView.swift", f'''import SwiftUI
import Domain

struct ContentView: View {{
    var body: some View {{
        NavigationStack {{
            Text("Welcome to {app_name}")
                .navigationTitle("{app_name}")
        }}
    }}
}}

#Preview {{
    ContentView()
}}
''')

    # Assets.xcassets/Contents.json
    write_file(f"{root}/Sources/App/Resources/Assets.xcassets/Contents.json", '''{
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
''')

    # AccentColor.colorset/Contents.json
    write_file(f"{root}/Sources/App/Resources/Assets.xcassets/AccentColor.colorset/Contents.json", '''{
  "colors" : [
    {
      "color" : {
        "color-space" : "srgb",
        "components" : {
          "alpha" : "1.000",
          "blue" : "0.400",
          "green" : "0.520",
          "red" : "0.000"
        }
      },
      "idiom" : "universal"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
''')

    # AppIcon.appiconset/Contents.json
    write_file(f"{root}/Sources/App/Resources/Assets.xcassets/AppIcon.appiconset/Contents.json", '''{
  "images" : [
    {
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
''')

    # Localizable.strings
    write_file(f"{root}/Sources/App/Resources/en.lproj/Localizable.strings", f'''/* General */
"app.name" = "{app_name}";
"common.cancel" = "Cancel";
"common.save" = "Save";
"common.edit" = "Edit";
"common.delete" = "Delete";
"common.back" = "Back";
''')

    # XCConfig - shared.xcconfig
    write_file(f"{root}/Sources/App/Resources/XCConfig/shared.xcconfig", f'''//  {app_name} shared.xcconfig
PRODUCT_BUNDLE_IDENTIFIER = {bundle_id}
DEVELOPMENT_TEAM = {team_id}
IPHONEOS_DEPLOYMENT_TARGET = 18.0
''')

    # XCConfig - debug.xcconfig
    write_file(f"{root}/Sources/App/Resources/XCConfig/debug.xcconfig", f'''//  {app_name} debug.xcconfig
#include "shared.xcconfig"

CODE_SIGN_IDENTITY = Apple Development
CODE_SIGN_STYLE = Automatic
''')

    # XCConfig - release.xcconfig
    write_file(f"{root}/Sources/App/Resources/XCConfig/release.xcconfig", f'''//  {app_name} release.xcconfig
#include "shared.xcconfig"

CODE_SIGN_IDENTITY = Apple Development
CODE_SIGN_STYLE = Automatic
''')

    # Domain - Example Model
    write_file(f"{root}/Sources/Domain/Models/Example.swift", '''import Foundation

/// Example domain model - replace with your actual models
public struct Example: Identifiable, Codable, Hashable, Sendable {
    public let id: UUID
    public var name: String
    public var createdAt: Date

    public init(id: UUID = UUID(), name: String, createdAt: Date = Date()) {
        self.id = id
        self.name = name
        self.createdAt = createdAt
    }
}
''')

    # Domain - Example Protocol
    write_file(f"{root}/Sources/Domain/Protocols/ExampleRepository.swift", '''import Foundation
import Mockable

/// Example repository protocol - replace with your actual protocols
@Mockable
public protocol ExampleRepository: Sendable {
    func fetchAll() async throws -> [Example]
    func save(_ item: Example) async throws
    func delete(_ item: Example) async throws
}
''')

    # Domain - Logger
    write_file(f"{root}/Sources/Domain/Utils/Logger+Domain.swift", f'''import Foundation
import OSLog

extension Logger {{
    static let domain = Logger(subsystem: "{bundle_id}", category: "domain")
}}
''')

    # Infrastructure - Example Repository
    write_file(f"{root}/Sources/Infrastructure/Local/LocalExampleRepository.swift", '''import Foundation
import Domain
import SwiftData

/// Example SwiftData repository - replace with your actual implementation
public final class LocalExampleRepository: ExampleRepository, @unchecked Sendable {
    public init() {}

    public func fetchAll() async throws -> [Example] {
        // TODO: Implement SwiftData fetching
        return []
    }

    public func save(_ item: Example) async throws {
        // TODO: Implement SwiftData saving
    }

    public func delete(_ item: Example) async throws {
        // TODO: Implement SwiftData deletion
    }
}
''')

    # Tests - Domain
    write_file(f"{root}/Tests/DomainTests/ExampleTests.swift", '''import Testing
import Foundation
@testable import Domain

struct ExampleTests {
    @Test func example_isIdentifiable() {
        let item1 = Example(name: "Test 1")
        let item2 = Example(name: "Test 2")

        #expect(item1.id != item2.id)
    }

    @Test func example_isCodable() throws {
        let original = Example(name: "Test")

        let encoder = JSONEncoder()
        let data = try encoder.encode(original)

        let decoder = JSONDecoder()
        let decoded = try decoder.decode(Example.self, from: data)

        #expect(decoded.id == original.id)
        #expect(decoded.name == original.name)
    }
}
''')

    # Tests - Infrastructure
    write_file(f"{root}/Tests/InfrastructureTests/LocalExampleRepositoryTests.swift", '''import Testing
import Foundation
@testable import Infrastructure
@testable import Domain

struct LocalExampleRepositoryTests {
    @Test func repository_placeholder() async throws {
        // TODO: Implement repository tests
    }
}
''')

    # README.md
    write_file(f"{root}/README.md", f'''# {app_name}

iOS app built with Swift 6 and Tuist.

## Requirements

- iOS 18.0+
- Xcode 16.0+
- Swift 6.0
- [Tuist](https://tuist.io)

## Getting Started

```bash
# Install Tuist
curl -Ls https://install.tuist.io | bash

# Generate Xcode project
tuist generate

# Open in Xcode
open {app_name}.xcworkspace
```

## Architecture

| Layer | Location | Purpose |
|-------|----------|---------|
| **Domain** | `Sources/Domain/` | Business logic, models, protocols |
| **Infrastructure** | `Sources/Infrastructure/` | Persistence, networking |
| **App** | `Sources/App/` | SwiftUI views, app entry |

## Project Structure

```
{app_name}/
├── Sources/
│   ├── App/           # SwiftUI views and app entry
│   ├── Domain/        # Business logic layer
│   └── Infrastructure/# Persistence layer
├── Tests/
│   ├── DomainTests/
│   └── InfrastructureTests/
├── Project.swift      # Tuist configuration
└── Tuist.swift
```
''')

    print(f"\n✅ {app_name} scaffolded successfully!")
    print(f"\nNext steps:")
    print(f"  cd {root}")
    print(f"  tuist generate")
    print(f"  open {app_name}.xcworkspace")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold an iOS app with Tuist")
    parser.add_argument("app_name", help="Name of the app")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--bundle-id", help="Bundle identifier (default: com.example.<appname>)")
    parser.add_argument("--team-id", default="YOUR_TEAM_ID", help="Development team ID")

    args = parser.parse_args()
    scaffold_app(args.app_name, args.output_dir, args.bundle_id, args.team_id)