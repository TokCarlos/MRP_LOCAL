Option Explicit

Dim fso, shell, root, cmdPath, args, rc
Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

root = fso.GetParentFolderName(WScript.ScriptFullName)
cmdPath = root & "\MRP_PAINEL_SERVIDOR.cmd"

If Not fso.FileExists(cmdPath) Then
    MsgBox "Launcher nao encontrado: " & cmdPath, vbCritical, "MRP_LOCAL - Painel do Servidor"
    WScript.Quit 1
End If

args = "cmd.exe /c """ & cmdPath & """"
rc = shell.Run(args, 0, True)
WScript.Quit rc

