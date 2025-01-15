#define MyAppName "Flowbite.Desktop"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Your Company Name"
#define MyAppExeName "Flowbite.Desktop.exe"

[Setup]
AppId={{GUID}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=dist\win-x46
OutputBaseFilename={#MyAppName}Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "src\AppServer\publish\AppServer.1.0.0.win-x64\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
