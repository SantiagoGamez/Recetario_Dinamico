[Setup]
AppName=Recipe Highlighter
AppVersion=1.0
AppPublisher=Your Name
AppPublisherURL=https://none.com
DefaultDirName={autopf}\RecipeConverter
DefaultGroupName=Recipe Converter
OutputDir=installer_output
OutputBaseFilename=RecipeConverter_Setup
SetupIconFile=recipe_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\RecipeConverter.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "recipe_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Recipe Converter"; Filename: "{app}\RecipeConverter.exe"; IconFilename: "{app}\recipe_icon.ico"
Name: "{autodesktop}\Recipe Converter"; Filename: "{app}\RecipeConverter.exe"; IconFilename: "{app}\recipe_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\RecipeConverter.exe"; Description: "{cm:LaunchProgram,Recipe Converter}"; Flags: nowait postinstall skipifsilent