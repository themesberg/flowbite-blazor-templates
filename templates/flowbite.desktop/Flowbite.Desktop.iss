; Version can be overridden by /DAppVersion=X.Y.Z command line parameter
#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif

#define MyAppName "Flowbite.Desktop"
#define MyAppPublisher "ACME"
#define MyAppURL "https://yourcompany.com"
#define MyAppExeName "Flowbite.Desktop.exe"

[Setup]
; Unique GUID for this application
AppId={{1234B321-1234-1234-1234-123456789ABC}}
AppName={#MyAppName}
AppVersion={#AppVersion}
AppVerName={#MyAppName} {#AppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
; Install to proper Program Files directory with publisher hierarchy
DefaultDirName={autopf}\{#MyAppPublisher}\{#MyAppName}
DefaultGroupName={#MyAppPublisher}\{#MyAppName}
; Ensure 64-bit installation
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
; Installer settings
OutputDir=dist\win-x64
OutputBaseFilename={#MyAppName}-{#AppVersion}-Setup
; Version information
VersionInfoVersion={#AppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} Installer
VersionInfoCopyright=© {#MyAppPublisher}
; Windows version requirements
MinVersion=10.0.17763
; Privileges required for installation
; Valid values: none, poweruser, admin, lowest
PrivilegesRequired=none
; Uninstall display settings
UninstallDisplayName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
; Allow user to change installation directory
AllowNoIcons=yes
; Prevent running multiple instances of installer
SetupMutex={#MyAppName}Setup
; Compression
Compression=lzma
SolidCompression=yes

[Files]
Source: "src\Flowbite.Desktop\publish\Flowbite.Desktop.{#AppVersion}.win-x64\Flowbite.Desktop.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\Flowbite.Desktop\publish\Flowbite.Desktop.{#AppVersion}.win-x64\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "Flowbite.Desktop.exe"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[InstallDelete]
; Clean up any old files during upgrade
Type: files; Name: "{app}\*"; 
Type: dirifempty; Name: "{app}"

[UninstallDelete]
; Clean up any remaining files
Type: files; Name: "{app}\*"
Type: dirifempty; Name: "{app}"

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
english.StartAfterInstall=Start %1 after installation

[Run]
; Run with elevated privileges after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:StartAfterInstall,{#MyAppName}}"; Flags: nowait postinstall skipifsilent shellexec
