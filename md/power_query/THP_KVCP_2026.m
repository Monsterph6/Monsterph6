section Section1;

shared Toncuoi = let
    Source = Folder.Files("C:\Users\phamh\OneDrive - Cong ty CP Kinh doanh than Mien Bac - Vinacomin\Thủy\KHO NĂM 2024\QTKVCP\tồn trạm\T12-New"),
    #"Filtered Hidden Files1" = Table.SelectRows(Source, each [Attributes]?[Hidden]? <> true),
    #"Invoke Custom Function1" = Table.AddColumn(#"Filtered Hidden Files1", "Transform File (2)", each #"Transform File (2)"([Content])),
    #"Renamed Columns1" = Table.RenameColumns(#"Invoke Custom Function1", {"Name", "Source.Name"}),
    #"Removed Other Columns1" = Table.SelectColumns(#"Renamed Columns1", {"Source.Name", "Transform File (2)"}),
    #"Expanded Table Column1" = Table.ExpandTableColumn(#"Removed Other Columns1", "Transform File (2)", Table.ColumnNames(#"Transform File (2)"(#"Sample File (2)"))),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Table Column1",{{"Source.Name", type text}, {"Column1", type any}, {"Column2", type any}, {"Column3", type any}, {"Column4", type any}, {"Column5", type any}, {"Column6", type any}, {"Column7", type any}, {"Column8", type any}, {"Column9", type any}, {"Column10", type any}, {"Column11", type any}, {"Column12", type any}, {"Column13", type any}, {"Column14", type any}, {"Column15", type any}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each ([Column2] <> null)),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Source.Name"}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Removed Columns", [PromoteAllScalars=true]),
    #"Removed Columns1" = Table.RemoveColumns(#"Promoted Headers",{"Cỡ hạt ", "Ghi chú", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15"}),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Columns1", each ([Số lượng] <> null and [Số lượng] <> "Số lượng" and [Số lượng] <> "Số lượng tồn theo sổ sách " and [Số lượng] <> "Tồn cuối kỳ") and ([Chủng loại] <> "Tổng" and [Chủng loại] <> "Tổng Cộng")),
    #"Rounded Off" = Table.TransformColumns(#"Filtered Rows1",{{"Số lượng", each Number.Round(_, 2), type number}, {"AK", each Number.Round(_, 2), type anynonnull}, {"Vk", each Number.Round(_, 2), type number}, {"Sk", each Number.Round(_, 2), type number}}),
    #"Rounded Off1" = Table.TransformColumns(#"Rounded Off",{{"Qk", each Number.Round(_, 0), type number}}),
    #"Merged Queries" = Table.NestedJoin(#"Rounded Off1", {"Chủng loại"}, Cam, {"Cam_all"}, "Cam", JoinKind.LeftOuter),
    #"Expanded Cam" = Table.ExpandTableColumn(#"Merged Queries", "Cam", {"Cam_B8"}, {"Cam.Cam_B8"}),
    #"Reordered Columns" = Table.ReorderColumns(#"Expanded Cam",{"STT", "Cam.Cam_B8", "Chủng loại", "Số lượng", "AK", "Vk", "Sk", "Qk"}),
    #"Removed Columns2" = Table.RemoveColumns(#"Reordered Columns",{"Chủng loại"}),
    #"Added Custom" = Table.AddColumn(#"Removed Columns2", "pr_ak", each [AK]*[Số lượng]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "pr_vk", each [Vk]*[Số lượng]),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "pr_sk", each [Sk]*[Số lượng]),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "pr_qk", each [Qk]*[Số lượng]),
    #"Removed Columns3" = Table.RemoveColumns(#"Added Custom3",{"AK", "Vk", "Sk", "Qk", "STT"}),
    #"Grouped Rows" = Table.Group(#"Removed Columns3", {"Cam.Cam_B8"}, {{"Luong", each List.Sum([Số lượng]), type number}, {"sak", each List.Sum([pr_ak]), type number}, {"svk", each List.Sum([pr_vk]), type number}, {"ssk", each List.Sum([pr_sk]), type number}, {"sqk", each List.Sum([pr_qk]), type number}}),
    #"Added Custom4" = Table.AddColumn(#"Grouped Rows", "Ak", each Number.Round([sak]/[Luong],2)),
    #"Added Custom5" = Table.AddColumn(#"Added Custom4", "Vk", each Number.Round([svk]/[Luong],2)),
    #"Added Custom6" = Table.AddColumn(#"Added Custom5", "Sk", each Number.Round([ssk]/[Luong],2)),
    #"Added Custom7" = Table.AddColumn(#"Added Custom6", "Qk", each Number.Round([sqk]/[Luong],0)),
    #"Removed Columns4" = Table.RemoveColumns(#"Added Custom7",{"sak", "svk", "ssk", "sqk"}),
    #"Sorted Rows" = Table.Sort(#"Removed Columns4",{{"Cam.Cam_B8", Order.Ascending}})
in
    #"Sorted Rows";

shared Parameter1 = #"Sample File" meta [IsParameterQuery=true, BinaryIdentifier=#"Sample File", Type="Binary", IsParameterQueryRequired=true];

shared #"Transform Sample File" = let
    Source = Excel.Workbook(Parameter1, null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data]
in
    Sheet1_Sheet;

shared #"Sample File" = let
    Source = Folder.Files("C:\Users\phamh\OneDrive - Cong ty CP Kinh doanh than Mien Bac - Vinacomin\Thủy\KHO NĂM 2024\QTKVCP\SỬA QTPT\tồn cl các trạm"),
    #"Filtered Hidden Files1" = Table.SelectRows(Source, each [Attributes]?[Hidden]? <> true),
    Navigation1 = #"Filtered Hidden Files1"{0}[Content]
in
    Navigation1;

[ FunctionQueryBinding = "{""exemplarFormulaName"":""Transform Sample File""}" ]
shared #"Transform File" = let
    Source = (Parameter1 as binary) => let
        Source = Excel.Workbook(Parameter1, null, true),
        Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data]
    in
        Sheet1_Sheet
in
    Source;

shared Cam = let
    Source = Excel.CurrentWorkbook(),
    Cam_B8 = Source{[Name="Cam_B8"]}[Content],
    #"Changed Type" = Table.TransformColumnTypes(Cam_B8,{{"Cam_all", type text}, {"B8", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"B8", "Cam_B8"}})
in
    #"Renamed Columns";

shared Tồn = let
    data = Excel.CurrentWorkbook(){[Name="forwpath"]}[Content],
    forwpath = data{0}[Column1],
    topath = forwpath & "Thủy\Path.xlsx",
    datapath = Excel.Workbook(File.Contents(topath), null, true),
    allpath = datapath{[Item="_2025",Kind="Table"]}[Data],
    backpath = allpath{5}[path],
    FilePath = forwpath & "Thủy\KHO NĂM 2026\QTTPT 2026\QTTPT 2026.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    Tồn_Sheet = Source{[Item="Tồn",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Tồn_Sheet, [PromoteAllScalars=true]),
    #"Added Custom" = Table.AddColumn(#"Promoted Headers", "T_Ak", each [L_T]*[Ak]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "T_Vk", each [Vk]*[L_T]),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "T_Qk", each [Qk]*[L_T]),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "T_Sk", each [Sk]*[L_T])
in
    #"Added Custom3";

shared Parameter2 = #"Sample File (2)" meta [IsParameterQuery=true, BinaryIdentifier=#"Sample File (2)", Type="Binary", IsParameterQueryRequired=true];

shared #"Transform Sample File (2)" = let
    Source = Excel.Workbook(Parameter2, null, true),
    Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data]
in
    Sheet1_Sheet;

shared #"Sample File (2)" = let
    Source = Folder.Files("C:\Users\phamh\OneDrive - Cong ty CP Kinh doanh than Mien Bac - Vinacomin\Thủy\KHO NĂM 2024\QTKVCP\SỬA QTPT\tồn cl các trạm"),
    Content0 = Source{0}[Content]
in
    Content0;

[ FunctionQueryBinding = "{""exemplarFormulaName"":""Transform Sample File (2)""}" ]
shared #"Transform File (2)" = let
    Source = (Parameter2 as binary) => let
        Source = Excel.Workbook(Parameter2, null, true),
        Sheet1_Sheet = Source{[Item="Sheet1",Kind="Sheet"]}[Data]
    in
        Sheet1_Sheet
in
    Source;

shared #"Toncuoi (3)" = let
    Source = Folder.Files("C:\Users\phamh\OneDrive - Cong ty CP Kinh doanh than Mien Bac - Vinacomin\Thủy\KHO NĂM 2024\QTKVCP\SỬA QTPT\tồn cl các trạm"),
    #"Filtered Hidden Files1" = Table.SelectRows(Source, each [Attributes]?[Hidden]? <> true),
    #"Invoke Custom Function1" = Table.AddColumn(#"Filtered Hidden Files1", "Transform File (2)", each #"Transform File (2)"([Content])),
    #"Renamed Columns1" = Table.RenameColumns(#"Invoke Custom Function1", {"Name", "Source.Name"}),
    #"Removed Other Columns1" = Table.SelectColumns(#"Renamed Columns1", {"Source.Name", "Transform File (2)"}),
    #"Expanded Table Column1" = Table.ExpandTableColumn(#"Removed Other Columns1", "Transform File (2)", Table.ColumnNames(#"Transform File (2)"(#"Sample File (2)"))),
    #"Changed Type" = Table.TransformColumnTypes(#"Expanded Table Column1",{{"Source.Name", type text}, {"Column1", type any}, {"Column2", type any}, {"Column3", type any}, {"Column4", type any}, {"Column5", type any}, {"Column6", type any}, {"Column7", type any}, {"Column8", type any}, {"Column9", type any}, {"Column10", type any}, {"Column11", type any}, {"Column12", type any}, {"Column13", type any}, {"Column14", type any}, {"Column15", type any}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each ([Column2] <> null)),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Source.Name"}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Removed Columns", [PromoteAllScalars=true]),
    #"Removed Columns1" = Table.RemoveColumns(#"Promoted Headers",{"Cỡ hạt ", "Ghi chú", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15"}),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Columns1", each ([Số lượng] <> null and [Số lượng] <> "Số lượng" and [Số lượng] <> "Số lượng tồn theo sổ sách " and [Số lượng] <> "Tồn cuối kỳ") and ([Chủng loại] <> "Tổng" and [Chủng loại] <> "Tổng Cộng")),
    #"Rounded Off" = Table.TransformColumns(#"Filtered Rows1",{{"Số lượng", each Number.Round(_, 2), type number}, {"AK", each Number.Round(_, 2), type anynonnull}, {"Vk", each Number.Round(_, 2), type number}, {"Sk", each Number.Round(_, 2), type number}}),
    #"Rounded Off1" = Table.TransformColumns(#"Rounded Off",{{"Qk", each Number.Round(_, 0), type number}}),
    #"Merged Queries" = Table.NestedJoin(#"Rounded Off1", {"Chủng loại"}, Cam, {"Cam_all"}, "Cam", JoinKind.LeftOuter),
    #"Expanded Cam" = Table.ExpandTableColumn(#"Merged Queries", "Cam", {"Cam_B8"}, {"Cam.Cam_B8"}),
    #"Removed Columns2" = Table.RemoveColumns(#"Expanded Cam",{"STT", "Số lượng", "AK", "Vk", "Sk", "Qk"}),
    #"Filtered Rows2" = Table.SelectRows(#"Removed Columns2", each ([Cam.Cam_B8] = null)),
    #"Removed Columns3" = Table.RemoveColumns(#"Filtered Rows2",{"Cam.Cam_B8"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns3")
in
    #"Removed Duplicates";

shared Bán = let
    data = Excel.CurrentWorkbook(){[Name="forwpath"]}[Content],
    forwpath = data{0}[Column1],
    topath = forwpath & "Thủy\Path.xlsx",
    datapath = Excel.Workbook(File.Contents(topath), null, true),
    allpath = datapath{[Item="_2025",Kind="Table"]}[Data],
    backpath = allpath{5}[path],
    FilePath = forwpath & "Thủy\KHO NĂM 2026\QTTPT 2026\QTTPT 2026.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    Bán_Sheet = Source{[Item="Bán",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Bán_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"SPT", Int64.Type}, {"N_HD", type date}, {"N_PT", type date}, {"N_NT", type date}, {"Tram", type text}, {"C_TP", type text}, {"C_PT", type text}, {"STTPA", Int64.Type}, {"Tháng", Int64.Type}, {"PL", type text}, {"C_B8", type text}, {"Ak", type number}, {"Vk", type number}, {"Sk", type number}, {"Qk", Int64.Type}, {"L_TTT", type number}, {"L_TTN", type number}, {"L_PA", type number}, {"L_HHB", type number}, {"L_KK", type number}, {"L_B", type number}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each [STTPA] < 0),
    #"Added Custom" = Table.AddColumn(#"Filtered Rows", "B_Ak", each [L_TTT]*[Ak]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "B_Vk", each [Vk]*[L_TTT]),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "B_Sk", each [Sk]*[L_TTT]),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "B_Qk", each [L_TTT]*[Qk])
in
    #"Added Custom3";

shared XPTTK = let
    Source = Excel.CurrentWorkbook(),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Name] = "'Bieu35a10 ĐHP'!Print_Area" or [Name] = "'Bieu35a10 ĐTB'!Print_Area" or [Name] = "'Bieu45a14 ĐHP'!Print_Area" or [Name] = "'Bieu45a14 ĐTB'!Print_Area" or [Name] = "'Bieu45a14 ĐVA'!Print_Area" or [Name] = "'Bieu76b1 (bán)'!Print_Area")),
    #"Expanded Content" = Table.ExpandTableColumn(#"Filtered Rows", "Content", {"Column1", "Column2", "Column3", "Column4", "Column5", "Column6", "Column7", "Column8", "Column9", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15", "Column16", "Column17", "Column18", "Column19", "Column20", "Column21", "Column22", "Column23", "Column24", "Column25", "Column26", "Column27", "Column28", "Column29", "Column30", "Column31", "Column32", "Column33", "Column34", "Column35", "Column36", "Column37", "Column38", "Column39", "Column40", "Column41", "Column42", "Column43", "Column44", "Column45", "Column46", "Column47", "Column48", "Column49", "Column50", "Column51", "Column52", "Column53", "Column54", "Column55", "Column56", "Column57", "Column58", "Column59", "Column60", "Column61", "Column62", "Column63", "Column64", "Column65", "Column66", "Column67", "Column68", "Column69", "Column70", "Column71", "Column72", "Column73", "Column74", "Column75", "Column76", "Column77", "Column78", "Column79", "Column80", "Column81", "Column82", "Column83", "Column84"}, {"Content.Column1", "Content.Column2", "Content.Column3", "Content.Column4", "Content.Column5", "Content.Column6", "Content.Column7", "Content.Column8", "Content.Column9", "Content.Column10", "Content.Column11", "Content.Column12", "Content.Column13", "Content.Column14", "Content.Column15", "Content.Column16", "Content.Column17", "Content.Column18", "Content.Column19", "Content.Column20", "Content.Column21", "Content.Column22", "Content.Column23", "Content.Column24", "Content.Column25", "Content.Column26", "Content.Column27", "Content.Column28", "Content.Column29", "Content.Column30", "Content.Column31", "Content.Column32", "Content.Column33", "Content.Column34", "Content.Column35", "Content.Column36", "Content.Column37", "Content.Column38", "Content.Column39", "Content.Column40", "Content.Column41", "Content.Column42", "Content.Column43", "Content.Column44", "Content.Column45", "Content.Column46", "Content.Column47", "Content.Column48", "Content.Column49", "Content.Column50", "Content.Column51", "Content.Column52", "Content.Column53", "Content.Column54", "Content.Column55", "Content.Column56", "Content.Column57", "Content.Column58", "Content.Column59", "Content.Column60", "Content.Column61", "Content.Column62", "Content.Column63", "Content.Column64", "Content.Column65", "Content.Column66", "Content.Column67", "Content.Column68", "Content.Column69", "Content.Column70", "Content.Column71", "Content.Column72", "Content.Column73", "Content.Column74", "Content.Column75", "Content.Column76", "Content.Column77", "Content.Column78", "Content.Column79", "Content.Column80", "Content.Column81", "Content.Column82", "Content.Column83", "Content.Column84"}),
    #"Replaced Errors" = Table.ReplaceErrorValues(#"Expanded Content", {{"Content.Column4", 0}, {"Content.Column5", 0}, {"Content.Column6", 0}, {"Content.Column7", 0}, {"Content.Column8", 0}, {"Content.Column9", 0}, {"Content.Column10", 0}, {"Content.Column11", 0}, {"Content.Column12", 0}, {"Content.Column13", 0}, {"Content.Column14", 0}, {"Content.Column15", 0}, {"Content.Column16", 0}, {"Content.Column17", 0}, {"Content.Column18", 0}, {"Content.Column19", 0}, {"Content.Column20", 0}, {"Content.Column21", 0}, {"Content.Column22", 0}, {"Content.Column23", 0}, {"Content.Column24", 0}, {"Content.Column25", 0}, {"Content.Column26", 0}, {"Content.Column27", 0}, {"Content.Column28", 0}, {"Content.Column29", 0}, {"Content.Column30", 0}, {"Content.Column31", 0}, {"Content.Column32", 0}, {"Content.Column33", 0}, {"Content.Column34", 0}, {"Content.Column35", 0}, {"Content.Column36", 0}, {"Content.Column37", 0}, {"Content.Column38", 0}, {"Content.Column39", 0}, {"Content.Column40", 0}, {"Content.Column41", 0}, {"Content.Column42", 0}, {"Content.Column43", 0}, {"Content.Column44", 0}, {"Content.Column45", 0}, {"Content.Column46", 0}, {"Content.Column47", 0}, {"Content.Column48", 0}, {"Content.Column49", 0}, {"Content.Column50", 0}, {"Content.Column51", 0}, {"Content.Column52", 0}, {"Content.Column53", 0}, {"Content.Column54", 0}, {"Content.Column55", 0}, {"Content.Column56", 0}, {"Content.Column57", 0}, {"Content.Column58", 0}, {"Content.Column59", 0}, {"Content.Column60", 0}, {"Content.Column61", 0}, {"Content.Column62", 0}, {"Content.Column63", 0}, {"Content.Column64", 0}, {"Content.Column65", 0}, {"Content.Column66", 0}, {"Content.Column67", 0}, {"Content.Column68", 0}, {"Content.Column69", 0}, {"Content.Column70", 0}, {"Content.Column71", 0}, {"Content.Column72", 0}, {"Content.Column73", 0}, {"Content.Column74", 0}, {"Content.Column75", 0}, {"Content.Column76", 0}, {"Content.Column77", 0}, {"Content.Column78", 0}, {"Content.Column79", 0}, {"Content.Column80", 0}, {"Content.Column81", 0}, {"Content.Column82", 0}, {"Content.Column83", 0}, {"Content.Column84", 0}}),
    #"Filtered Rows1" = Table.SelectRows(#"Replaced Errors", each ([Content.Column5] <> null)),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows1",{"Content.Column9", "Content.Column10", "Content.Column11", "Content.Column12", "Content.Column13", "Content.Column14", "Content.Column15", "Content.Column16", "Content.Column17", "Content.Column18", "Content.Column19", "Content.Column20", "Content.Column21", "Content.Column22", "Content.Column23", "Content.Column24", "Content.Column25", "Content.Column26", "Content.Column27", "Content.Column28", "Content.Column29", "Content.Column30", "Content.Column31", "Content.Column32", "Content.Column33", "Content.Column34", "Content.Column35", "Content.Column36", "Content.Column37", "Content.Column38", "Content.Column39", "Content.Column40", "Content.Column41", "Content.Column42", "Content.Column43", "Content.Column44", "Content.Column45", "Content.Column46", "Content.Column47", "Content.Column48", "Content.Column49", "Content.Column50", "Content.Column51", "Content.Column52", "Content.Column53", "Content.Column54", "Content.Column55", "Content.Column56", "Content.Column57", "Content.Column58", "Content.Column59", "Content.Column60", "Content.Column61", "Content.Column62", "Content.Column63", "Content.Column64", "Content.Column65", "Content.Column66", "Content.Column67", "Content.Column68"}),
    #"Filtered Rows2" = Table.SelectRows(#"Removed Columns", each ([Content.Column2] = null) and ([Content.Column3] <> null)),
    #"Merged Queries" = Table.NestedJoin(#"Filtered Rows2", {"Name"}, #"XPTTK (2)", {"Name"}, "XPTTK (2)", JoinKind.LeftOuter),
    #"Expanded XPTTK (2)" = Table.ExpandTableColumn(#"Merged Queries", "XPTTK (2)", {"Name - Copy"}, {"XPTTK (2).Name - Copy"}),
    #"Removed Columns1" = Table.RemoveColumns(#"Expanded XPTTK (2)",{"Name"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns1",{{"XPTTK (2).Name - Copy", "CTP"}, {"Content.Column4", "L_B"}, {"Content.Column5", "Ak_B"}, {"Content.Column6", "VK_B"}, {"Content.Column7", "QK_B"}, {"Content.Column8", "SK_B"}}),
    #"Removed Columns2" = Table.RemoveColumns(#"Renamed Columns",{"Content.Column1", "Content.Column2", "Content.Column69"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns2",{{"Content.Column70", "L_T"}, {"Content.Column71", "AL_T"}, {"Content.Column72", "VK_T"}, {"Content.Column73", "QK_T"}, {"Content.Column74", "SK_T"}}),
    #"Filtered Rows3" = Table.SelectRows(#"Renamed Columns1", each ([Content.Column3] <> "Phòng KHKD" and [Content.Column3] <> "Trần Ngọc Phong") and ([L_B] <> null))
in
    #"Filtered Rows3";

shared #"XPTTK (2)" = let
    Source = Excel.CurrentWorkbook(),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Name] = "'Bieu35a10 ĐHP'!Print_Area" or [Name] = "'Bieu35a10 ĐTB'!Print_Area" or [Name] = "'Bieu45a14 ĐHP'!Print_Area" or [Name] = "'Bieu45a14 ĐTB'!Print_Area" or [Name] = "'Bieu45a14 ĐVA'!Print_Area" or [Name] = "'Bieu76b1 (bán)'!Print_Area")),
    #"Expanded Content" = Table.ExpandTableColumn(#"Filtered Rows", "Content", {"Column1", "Column2", "Column3", "Column4", "Column5", "Column6", "Column7", "Column8", "Column9", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15", "Column16", "Column17", "Column18", "Column19", "Column20", "Column21", "Column22", "Column23", "Column24", "Column25", "Column26", "Column27", "Column28", "Column29", "Column30", "Column31", "Column32", "Column33", "Column34", "Column35", "Column36", "Column37", "Column38", "Column39", "Column40", "Column41", "Column42", "Column43", "Column44", "Column45", "Column46", "Column47", "Column48", "Column49", "Column50", "Column51", "Column52", "Column53", "Column54", "Column55", "Column56", "Column57", "Column58", "Column59", "Column60", "Column61", "Column62", "Column63", "Column64", "Column65", "Column66", "Column67", "Column68", "Column69", "Column70", "Column71", "Column72", "Column73", "Column74", "Column75", "Column76", "Column77", "Column78", "Column79", "Column80", "Column81", "Column82", "Column83", "Column84"}, {"Content.Column1", "Content.Column2", "Content.Column3", "Content.Column4", "Content.Column5", "Content.Column6", "Content.Column7", "Content.Column8", "Content.Column9", "Content.Column10", "Content.Column11", "Content.Column12", "Content.Column13", "Content.Column14", "Content.Column15", "Content.Column16", "Content.Column17", "Content.Column18", "Content.Column19", "Content.Column20", "Content.Column21", "Content.Column22", "Content.Column23", "Content.Column24", "Content.Column25", "Content.Column26", "Content.Column27", "Content.Column28", "Content.Column29", "Content.Column30", "Content.Column31", "Content.Column32", "Content.Column33", "Content.Column34", "Content.Column35", "Content.Column36", "Content.Column37", "Content.Column38", "Content.Column39", "Content.Column40", "Content.Column41", "Content.Column42", "Content.Column43", "Content.Column44", "Content.Column45", "Content.Column46", "Content.Column47", "Content.Column48", "Content.Column49", "Content.Column50", "Content.Column51", "Content.Column52", "Content.Column53", "Content.Column54", "Content.Column55", "Content.Column56", "Content.Column57", "Content.Column58", "Content.Column59", "Content.Column60", "Content.Column61", "Content.Column62", "Content.Column63", "Content.Column64", "Content.Column65", "Content.Column66", "Content.Column67", "Content.Column68", "Content.Column69", "Content.Column70", "Content.Column71", "Content.Column72", "Content.Column73", "Content.Column74", "Content.Column75", "Content.Column76", "Content.Column77", "Content.Column78", "Content.Column79", "Content.Column80", "Content.Column81", "Content.Column82", "Content.Column83", "Content.Column84"}),
    #"Replaced Errors" = Table.ReplaceErrorValues(#"Expanded Content", {{"Content.Column4", 0}, {"Content.Column5", 0}, {"Content.Column6", 0}, {"Content.Column7", 0}, {"Content.Column8", 0}, {"Content.Column9", 0}, {"Content.Column10", 0}, {"Content.Column11", 0}, {"Content.Column12", 0}, {"Content.Column13", 0}, {"Content.Column14", 0}, {"Content.Column15", 0}, {"Content.Column16", 0}, {"Content.Column17", 0}, {"Content.Column18", 0}, {"Content.Column19", 0}, {"Content.Column20", 0}, {"Content.Column21", 0}, {"Content.Column22", 0}, {"Content.Column23", 0}, {"Content.Column24", 0}, {"Content.Column25", 0}, {"Content.Column26", 0}, {"Content.Column27", 0}, {"Content.Column28", 0}, {"Content.Column29", 0}, {"Content.Column30", 0}, {"Content.Column31", 0}, {"Content.Column32", 0}, {"Content.Column33", 0}, {"Content.Column34", 0}, {"Content.Column35", 0}, {"Content.Column36", 0}, {"Content.Column37", 0}, {"Content.Column38", 0}, {"Content.Column39", 0}, {"Content.Column40", 0}, {"Content.Column41", 0}, {"Content.Column42", 0}, {"Content.Column43", 0}, {"Content.Column44", 0}, {"Content.Column45", 0}, {"Content.Column46", 0}, {"Content.Column47", 0}, {"Content.Column48", 0}, {"Content.Column49", 0}, {"Content.Column50", 0}, {"Content.Column51", 0}, {"Content.Column52", 0}, {"Content.Column53", 0}, {"Content.Column54", 0}, {"Content.Column55", 0}, {"Content.Column56", 0}, {"Content.Column57", 0}, {"Content.Column58", 0}, {"Content.Column59", 0}, {"Content.Column60", 0}, {"Content.Column61", 0}, {"Content.Column62", 0}, {"Content.Column63", 0}, {"Content.Column64", 0}, {"Content.Column65", 0}, {"Content.Column66", 0}, {"Content.Column67", 0}, {"Content.Column68", 0}, {"Content.Column69", 0}, {"Content.Column70", 0}, {"Content.Column71", 0}, {"Content.Column72", 0}, {"Content.Column73", 0}, {"Content.Column74", 0}, {"Content.Column75", 0}, {"Content.Column76", 0}, {"Content.Column77", 0}, {"Content.Column78", 0}, {"Content.Column79", 0}, {"Content.Column80", 0}, {"Content.Column81", 0}, {"Content.Column82", 0}, {"Content.Column83", 0}, {"Content.Column84", 0}}),
    #"Filtered Rows1" = Table.SelectRows(#"Replaced Errors", each ([Content.Column5] <> null)),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows1",{"Content.Column9", "Content.Column10", "Content.Column11", "Content.Column12", "Content.Column13", "Content.Column14", "Content.Column15", "Content.Column16", "Content.Column17", "Content.Column18", "Content.Column19", "Content.Column20", "Content.Column21", "Content.Column22", "Content.Column23", "Content.Column24", "Content.Column25", "Content.Column26", "Content.Column27", "Content.Column28", "Content.Column29", "Content.Column30", "Content.Column31", "Content.Column32", "Content.Column33", "Content.Column34", "Content.Column35", "Content.Column36", "Content.Column37", "Content.Column38", "Content.Column39", "Content.Column40", "Content.Column41", "Content.Column42", "Content.Column43", "Content.Column44", "Content.Column45", "Content.Column46", "Content.Column47", "Content.Column48", "Content.Column49", "Content.Column50", "Content.Column51", "Content.Column52", "Content.Column53", "Content.Column54", "Content.Column55", "Content.Column56", "Content.Column57", "Content.Column58", "Content.Column59", "Content.Column60", "Content.Column61", "Content.Column62", "Content.Column63", "Content.Column64", "Content.Column65", "Content.Column66", "Content.Column67", "Content.Column68"}),
    #"Filtered Rows2" = Table.SelectRows(#"Removed Columns", each ([Content.Column2] = null) and ([Content.Column3] <> null)),
    #"Removed Columns1" = Table.RemoveColumns(#"Filtered Rows2",{"Content.Column1", "Content.Column2", "Content.Column3", "Content.Column4", "Content.Column5", "Content.Column6", "Content.Column7", "Content.Column8", "Content.Column69", "Content.Column70", "Content.Column71", "Content.Column72", "Content.Column73", "Content.Column74", "Content.Column75", "Content.Column76", "Content.Column77", "Content.Column78", "Content.Column79", "Content.Column80", "Content.Column81", "Content.Column82", "Content.Column83", "Content.Column84"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns1"),
    #"Duplicated Column" = Table.DuplicateColumn(#"Removed Duplicates", "Name", "Name - Copy"),
    #"Replaced Value" = Table.ReplaceValue(#"Duplicated Column","'Bieu35a10 ĐTB'!Print_Area","5a.10 ĐTB",Replacer.ReplaceText,{"Name - Copy"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value","'Bieu45a14 ĐHP'!Print_Area","5a.14 ĐHP",Replacer.ReplaceText,{"Name - Copy"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","'Bieu45a14 ĐTB'!Print_Area","5a.14 ĐTB",Replacer.ReplaceText,{"Name - Copy"}),
    #"Replaced Value3" = Table.ReplaceValue(#"Replaced Value2","'Bieu45a14 ĐVA'!Print_Area","5a.14 ĐVA",Replacer.ReplaceText,{"Name - Copy"}),
    #"Replaced Value4" = Table.ReplaceValue(#"Replaced Value3","'Bieu76b1 (bán)'!Print_Area","6b.1 ĐHD",Replacer.ReplaceText,{"Name - Copy"}),
    #"Replaced Value5" = Table.ReplaceValue(#"Replaced Value4","'Bieu35a10 ĐHP'!Print_Area","5a.10 ĐHP",Replacer.ReplaceText,{"Name - Copy"})
in
    #"Replaced Value5";

shared B8_NT = let
    Source = Excel.Workbook(File.Contents("C:\Users\phamh\OneDrive\Thủy\KHO NĂM 2025\QTTPT 2025\KVCP\THP.Biểu mẫu Quyết toán KVCP 2025.xlsx"), null, true),
    #"Bieu8 canbangchat_Sheet" = Source{[Item="Bieu8 canbangchat",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(#"Bieu8 canbangchat_Sheet",{{"Column1", type any}, {"Column2", type any}, {"Column3", type any}, {"Column4", type any}, {"Column5", type any}, {"Column6", type any}, {"Column7", type any}, {"Column8", type any}, {"Column9", type any}, {"Column10", type any}, {"Column11", type any}, {"Column12", type any}, {"Column13", type any}, {"Column14", type any}, {"Column15", type any}, {"Column16", type any}, {"Column17", type any}, {"Column18", type any}, {"Column19", type any}, {"Column20", type any}, {"Column21", type any}, {"Column22", type any}, {"Column23", type any}, {"Column24", type any}, {"Column25", type any}, {"Column26", type any}, {"Column27", type any}, {"Column28", type any}, {"Column29", type any}, {"Column30", type any}, {"Column31", type any}, {"Column32", type any}, {"Column33", type any}, {"Column34", type any}, {"Column35", type any}, {"Column36", type any}, {"Column37", type any}, {"Column38", type any}, {"Column39", type any}, {"Column40", type any}, {"Column41", type any}, {"Column42", type any}, {"Column43", type any}, {"Column44", type any}, {"Column45", type any}, {"Column46", type any}, {"Column47", type any}, {"Column48", type any}, {"Column49", type number}, {"Column50", type any}, {"Column51", type any}, {"Column52", type any}, {"Column53", type any}, {"Column54", type any}, {"Column55", type any}, {"Column56", type any}, {"Column57", type any}, {"Column58", type any}, {"Column59", type any}, {"Column60", type any}, {"Column61", type any}, {"Column62", type any}, {"Column63", type any}, {"Column64", type any}, {"Column65", type any}, {"Column66", type any}, {"Column67", type any}, {"Column68", type any}, {"Column69", type any}, {"Column70", type any}, {"Column71", type any}, {"Column72", type any}, {"Column73", type any}, {"Column74", type any}, {"Column75", type any}, {"Column76", type any}, {"Column77", type any}, {"Column78", type any}, {"Column79", type any}, {"Column80", type any}, {"Column81", type any}, {"Column82", type any}, {"Column83", type any}, {"Column84", type any}, {"Column85", type any}, {"Column86", type any}, {"Column87", type any}, {"Column88", type any}, {"Column89", type any}, {"Column90", type number}, {"Column91", type number}, {"Column92", type number}, {"Column93", type any}, {"Column94", type any}, {"Column95", type any}, {"Column96", type any}, {"Column97", type any}, {"Column98", type any}, {"Column99", type any}, {"Column100", type any}, {"Column101", type any}, {"Column102", type any}, {"Column103", type any}, {"Column104", type any}, {"Column105", type any}, {"Column106", type any}, {"Column107", type any}, {"Column108", type any}, {"Column109", type any}, {"Column110", type any}, {"Column111", type any}, {"Column112", type number}, {"Column113", type number}, {"Column114", type number}, {"Column115", type number}, {"Column116", type number}, {"Column117", Int64.Type}, {"Column118", type number}, {"Column119", type any}, {"Column120", type any}, {"Column121", type any}, {"Column122", type any}, {"Column123", type any}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each ([Column2] <> null)),
    #"Promoted Headers" = Table.PromoteHeaders(#"Filtered Rows", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers",{{"TT", type any}, {"Loại than", type any}, {"Tồn đầu kỳ", type number}, {"Column4", type number}, {"Column5", type number}, {"Column6", type number}, {"Column7", type number}, {"Than nhập trong kỳ", type number}, {"Column9", type number}, {"Column10", type number}, {"Column11", type number}, {"Column12", type number}, {"Column13", type number}, {"Column14", type number}, {"Column15", type number}, {"Column16", type number}, {"Column17", type number}, {"Than nhập trong kỳ_1", type number}, {"Column19", type number}, {"Column20", type number}, {"Column21", type number}, {"Column22", type number}, {"Column23", Int64.Type}, {"Column24", Int64.Type}, {"Column25", Int64.Type}, {"Column26", Int64.Type}, {"Column27", Int64.Type}, {"Column28", type number}, {"Column29", type number}, {"Column30", type number}, {"Column31", type number}, {"Column32", type number}, {"Than nhập trong kỳ_2", Int64.Type}, {"Column34", Int64.Type}, {"Column35", Int64.Type}, {"Column36", Int64.Type}, {"Column37", Int64.Type}, {"Tổng nhập", type number}, {"Column39", type number}, {"Column40", type number}, {"Column41", type number}, {"Column42", type number}, {"Tổng xuất", type number}, {"Column44", type number}, {"Column45", type number}, {"Column46", type number}, {"Column47", type number}, {"Column48", type any}, {"Column49", type number}, {"Than xuất trong kỳ", type number}, {"Column51", type number}, {"Column52", type number}, {"Column53", type number}, {"Column54", type number}, {"Column55", Int64.Type}, {"Column56", Int64.Type}, {"Column57", Int64.Type}, {"Column58", Int64.Type}, {"Column59", Int64.Type}, {"Column60", type number}, {"Column61", type number}, {"Column62", type number}, {"Column63", type number}, {"Column64", type number}, {"Than xuất trong kỳ_3", type number}, {"Column66", type number}, {"Column67", type number}, {"Column68", type number}, {"Column69", type number}, {"Column70", Int64.Type}, {"Column71", Int64.Type}, {"Column72", Int64.Type}, {"Column73", Int64.Type}, {"Column74", Int64.Type}, {"Column75", Int64.Type}, {"Column76", Int64.Type}, {"Column77", Int64.Type}, {"Column78", Int64.Type}, {"Column79", Int64.Type}, {"Tồn thống kê", type number}, {"Column81", type number}, {"Column82", type number}, {"Column83", type number}, {"Column84", type number}, {"Tồn cuối kỳ ", type number}, {"Column86", type number}, {"Column87", type number}, {"Column88", type number}, {"Column89", type number}, {"Column90", type number}, {"Column91", type number}, {"Column92", type number}, {"Chênh lệch", type number}, {"Column94", type number}, {"Column95", type number}, {"Column96", type number}, {"Column97", type number}, {"Diễn giải tồn cuối t12", type number}, {"Tồn cuối kỳ", type number}, {"Column100", type any}, {"Column101", Int64.Type}, {"Column102", type any}, {"Hao hụt", type any}, {"Column104", type any}, {"Column105", type any}, {"Column106", type any}, {"Check", type any}, {"Column108", type number}, {"Column109", type number}, {"Column110", type number}, {"Column111", type number}, {"Column112", type number}, {"Column113", type number}, {"Column114", type number}, {"Column115", type number}, {"Column116", type number}, {"Column117", Int64.Type}, {"Column118", type number}, {"Column119", type any}, {"Column120", type any}, {"Column121", type any}, {"Column122", type any}, {"Column123", type any}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type1",{"Column90", "Column91", "Column92", "Chênh lệch", "Column94", "Column95", "Column96", "Column97", "Diễn giải tồn cuối t12", "Tồn cuối kỳ", "Column100", "Column101", "Column102", "Hao hụt", "Column104", "Column105", "Column106", "Check", "Column108", "Column109", "Column110", "Column111", "Column112", "Column113", "Column114", "Column115", "Column116", "Column117", "Column118", "Column119", "Column120", "Column121", "Column122", "Column123", "Tồn đầu kỳ", "Column4", "Column5", "Column6", "Column7", "Than nhập trong kỳ", "Column9", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15", "Column16", "Column17", "Than nhập trong kỳ_1", "Column19", "Column20", "Column21", "Column22", "Column23", "Column24", "Column25", "Column26", "Column27", "Column28", "Column29", "Column30", "Column31", "Column32", "Than nhập trong kỳ_2", "Column34", "Column35", "Column36", "Column37", "Tổng nhập", "Column39", "Column40", "Column41", "Column42", "Tổng xuất", "Column44", "Column45", "Column46", "Column47", "Column48", "Column49", "Than xuất trong kỳ", "Column51", "Column52", "Column53", "Column54", "Column55", "Column56", "Column57", "Column58", "Column59", "Column60", "Column61", "Column62", "Column63", "Column64", "Than xuất trong kỳ_3", "Column66", "Column67", "Column68", "Column69", "Column70", "Column71", "Column72", "Column73", "Column74", "Column75", "Column76", "Column77", "Column78", "Column79", "Tồn thống kê", "Column81", "Column82", "Column83", "Column84"}),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Columns", each ([#"Tồn cuối kỳ "] <> null and [#"Tồn cuối kỳ "] <> 0) and ([Loại than] <> 2 and [Loại than] <> "Than cám" and [Loại than] <> "Than cám PTNK" and [Loại than] <> "Than nhập khẩu" and [Loại than] <> "Than sạch tổng số" and [Loại than] <> "Than TCCS" and [Loại than] <> "Than TCVN")),
    #"Removed Columns1" = Table.RemoveColumns(#"Filtered Rows1",{"TT"}),
    #"Rounded Off" = Table.TransformColumns(#"Removed Columns1",{{"Tồn cuối kỳ ", each Number.Round(_, 2), type number}, {"Column86", each Number.Round(_, 2), type number}, {"Column87", each Number.Round(_, 2), type number}}),
    #"Rounded Off1" = Table.TransformColumns(#"Rounded Off",{{"Column89", each Number.Round(_, 2), type number}}),
    #"Rounded Off2" = Table.TransformColumns(#"Rounded Off1",{{"Column88", each Number.Round(_, 0), type number}})
in
    #"Rounded Off2";

shared CN = let
    data = Excel.CurrentWorkbook(){[Name="forwpath"]}[Content],
    forwpath = data{0}[Column1],
    topath = forwpath & "Thủy\Path.xlsx",
    datapath = Excel.Workbook(File.Contents(topath), null, true),
    allpath = datapath{[Item="_2025",Kind="Table"]}[Data],
    backpath = allpath{5}[path],
    FilePath = forwpath & "Thủy\KHO NĂM 2026\QTTPT 2026\QTTPT 2026.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    Bán_Sheet = Source{[Item="XCN",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Bán_Sheet, [PromoteAllScalars=true]),
    #"Removed Columns" = Table.RemoveColumns(#"Promoted Headers",{"L_100"}),
    #"Added Custom" = Table.AddColumn(#"Removed Columns", "CN_AK", each [L_T]*[Ak]),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "CN_VK", each [L_T]*[Vk]),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "CN_SK", each [L_T]*[Sk]),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "CN_QK", each [Qk]*[L_T])
in
    #"Added Custom3";