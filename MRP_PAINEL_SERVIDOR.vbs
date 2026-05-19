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

If rc <> 0 Then
    MsgBox "Falha ao abrir o painel. Codigo: " & rc & vbCrLf & "Verifique o arquivo launcher_painel.log em 01-mrp\logs\admin.", vbExclamation, "MRP_LOCAL - Painel do Servidor"
End If

WScript.Quit rc

