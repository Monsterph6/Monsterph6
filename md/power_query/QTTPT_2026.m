section Section1;

shared PA = let
    data = Excel.CurrentWorkbook(){[Name="forwpath"]}[Content],
    forwpath = data{0}[Column1],
    FilePath = forwpath & "8. Thủy\KHO NĂM 2026\Sổ theo dõi PA trạm 2026.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Name] = "T1" or [Name] = "T2" or [Name] = "T3" or [Name] = "T4" or [Name] = "T5" or [Name] = "T6" or [Name] = "T7" or [Name] = "T8" or [Name] = "T9" or [Name] = "T10" or [Name] = "T11" or [Name] = "T12")),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Item", "Kind", "Hidden"}),
    #"Expanded Data" = Table.ExpandTableColumn(#"Removed Columns", "Data", {"Column1", "Column2", "Column3", "Column4", "Column5", "Column6", "Column7", "Column8", "Column9", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15", "Column16", "Column17", "Column18", "Column19", "Column20", "Column21", "Column22", "Column23", "Column24", "Column25", "Column26", "Column27", "Column28", "Column29", "Column30"}, {"Data.Column1", "Data.Column2", "Data.Column3", "Data.Column4", "Data.Column5", "Data.Column6", "Data.Column7", "Data.Column8", "Data.Column9", "Data.Column10", "Data.Column11", "Data.Column12", "Data.Column13", "Data.Column14", "Data.Column15", "Data.Column16", "Data.Column17", "Data.Column18", "Data.Column19", "Data.Column20", "Data.Column21", "Data.Column22", "Data.Column23", "Data.Column24", "Data.Column25", "Data.Column26", "Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30"}),
    #"Added Custom" = Table.AddColumn(#"Expanded Data", "Custom", each Text.Select([Name],{"0".."9"})),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"Custom", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Custom", "Tháng"}}),
    #"Removed Columns1" = Table.RemoveColumns(#"Renamed Columns",{"Name"}),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Columns1", each ([Data.Column29] = 2) and ([Data.Column28] = "") and ([Data.Column7] <> null)),
    #"Added Custom2" = Table.AddColumn(#"Filtered Rows1", "Cảng", each if [Data.Column18]="Cảng chính" then "CC" else ""),
    #"Removed Columns2" = Table.RemoveColumns(#"Added Custom2",{"Data.Column15", "Data.Column16", "Data.Column17", "Data.Column18", "Data.Column19", "Data.Column20", "Data.Column21", "Data.Column22", "Data.Column23", "Data.Column24", "Data.Column25", "Data.Column26", "Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Removed Columns2",{{"Data.Column1", Int64.Type}}),
    #"Removed Columns3" = Table.RemoveColumns(#"Changed Type1",{"Data.Column8"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns3",{{"Data.Column1", "SPT"}, {"Data.Column2", "N_HD"}, {"Data.Column3", "N_PT"}, {"Data.Column4", "N_NT"}, {"Data.Column5", "Tram"}, {"Data.Column9", "L_100"}, {"Data.Column10", "Ak"}, {"Data.Column11", "Vk"}, {"Data.Column12", "Sk"}, {"Data.Column13", "Qk"}, {"Data.Column14", "L_NT"}}),
    #"Sorted Rows" = Table.Sort(#"Renamed Columns1",{{"Tháng", Order.Ascending}, {"Tram", Order.Ascending}, {"SPT", Order.Ascending}}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Sorted Rows",{{"N_HD", type date}, {"N_PT", type date}, {"N_NT", type date}}),
    #"Added Custom1" = Table.AddColumn(#"Changed Type2", "Merge", each Text.From([SPT]) & "|" & Text.From([Tram])& "|" & Text.From([Tháng])),
    #"Merged Queries" = Table.NestedJoin(#"Added Custom1", {"Merge"}, Index, {"Merge"}, "Index", JoinKind.LeftOuter),
    #"Expanded Index" = Table.ExpandTableColumn(#"Merged Queries", "Index", {"Index"}, {"Index.Index"}),
    #"Renamed Columns2" = Table.RenameColumns(#"Expanded Index",{{"Index.Index", "STTPA"}}),
    #"Removed Columns4" = Table.RemoveColumns(#"Renamed Columns2",{"Merge"}),
    #"Reordered Columns" = Table.ReorderColumns(#"Removed Columns4",{"SPT", "N_HD", "N_PT", "N_NT", "Tram", "Data.Column6", "Data.Column7", "L_100", "Ak", "Vk", "Sk", "Qk", "L_NT", "STTPA", "Tháng"}),
    #"Trimmed Text" = Table.TransformColumns(#"Reordered Columns",{{"Data.Column7", Text.Trim, type text}})
in
    #"Trimmed Text";

shared Than = let
    data = Excel.CurrentWorkbook(){[Name="forwpath"]}[Content],
    forwpath = data{0}[Column1],
    FilePath = forwpath & "8. Thủy\KHO NĂM 2026\Sổ theo dõi PA trạm 2026.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Name] = "T1" or [Name] = "T2" or [Name] = "T3" or [Name] = "T4" or [Name] = "T5" or [Name] = "T6" or [Name] = "T7" or [Name] = "T8" or [Name] = "T9" or [Name] = "T10" or [Name] = "T11" or [Name] = "T12")),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Item", "Kind", "Hidden"}),
    #"Expanded Data" = Table.ExpandTableColumn(#"Removed Columns", "Data", {"Column1", "Column2", "Column3", "Column4", "Column5", "Column6", "Column7", "Column8", "Column9", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15", "Column16", "Column17", "Column18", "Column19", "Column20", "Column21", "Column22", "Column23", "Column24", "Column25", "Column26", "Column27", "Column28", "Column29", "Column30"}, {"Data.Column1", "Data.Column2", "Data.Column3", "Data.Column4", "Data.Column5", "Data.Column6", "Data.Column7", "Data.Column8", "Data.Column9", "Data.Column10", "Data.Column11", "Data.Column12", "Data.Column13", "Data.Column14", "Data.Column15", "Data.Column16", "Data.Column17", "Data.Column18", "Data.Column19", "Data.Column20", "Data.Column21", "Data.Column22", "Data.Column23", "Data.Column24", "Data.Column25", "Data.Column26", "Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30"}),
    #"Added Custom" = Table.AddColumn(#"Expanded Data", "Custom", each Text.Select([Name],{"0".."9"})),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"Custom", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Custom", "Tháng"}}),
    #"Removed Columns1" = Table.RemoveColumns(#"Renamed Columns",{"Name"}),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Columns1", each ([Data.Column29] = 2) and ([Data.Column28] = "") and ([Data.Column7] <> null)),
    #"Removed Columns2" = Table.RemoveColumns(#"Filtered Rows1",{"Data.Column15", "Data.Column16", "Data.Column17", "Data.Column18", "Data.Column19", "Data.Column20", "Data.Column21", "Data.Column22", "Data.Column23", "Data.Column24", "Data.Column25", "Data.Column26", "Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Removed Columns2",{{"Data.Column1", Int64.Type}}),
    #"Removed Columns3" = Table.RemoveColumns(#"Changed Type1",{"Data.Column8"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns3",{{"Data.Column1", "SPT"}, {"Data.Column2", "N_HD"}, {"Data.Column3", "N_PT"}, {"Data.Column4", "N_NT"}, {"Data.Column5", "Tram"}, {"Data.Column9", "L_100"}, {"Data.Column10", "Ak"}, {"Data.Column11", "Vk"}, {"Data.Column12", "Sk"}, {"Data.Column13", "Qk"}, {"Data.Column14", "L_NT"}}),
    #"Sorted Rows" = Table.Sort(#"Renamed Columns1",{{"Tháng", Order.Ascending}, {"Tram", Order.Ascending}, {"SPT", Order.Ascending}}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Sorted Rows",{{"N_HD", type date}, {"N_PT", type date}, {"N_NT", type date}}),
    #"Replaced Errors1" = Table.ReplaceErrorValues(#"Changed Type2", {{"Data.Column6", null}}),
    #"Removed Columns4" = Table.RemoveColumns(#"Replaced Errors1",{"SPT", "N_HD", "N_PT", "N_NT", "Tram", "L_100", "Ak", "Vk", "Sk", "Qk", "L_NT", "Tháng"}),
    #"Replaced Errors" = Table.ReplaceErrorValues(#"Removed Columns4", {{"Data.Column6", null}}),
    #"Filtered Rows2" = Table.SelectRows(#"Replaced Errors", each true),
    #"Removed Duplicates" = Table.Distinct(#"Filtered Rows2")
in
    #"Removed Duplicates";

shared Index = let
    data = Excel.CurrentWorkbook(){[Name="forwpath"]}[Content],
    forwpath = data{0}[Column1],
    FilePath = forwpath & "8. Thủy\KHO NĂM 2026\Sổ theo dõi PA trạm 2026.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Name] = "T1" or [Name] = "T2" or [Name] = "T3" or [Name] = "T4" or [Name] = "T5" or [Name] = "T6" or [Name] = "T7" or [Name] = "T8" or [Name] = "T9" or [Name] = "T10" or [Name] = "T11" or [Name] = "T12")),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Item", "Kind", "Hidden"}),
    #"Expanded Data" = Table.ExpandTableColumn(#"Removed Columns", "Data", {"Column1", "Column2", "Column3", "Column4", "Column5", "Column6", "Column7", "Column8", "Column9", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15", "Column16", "Column17", "Column18", "Column19", "Column20", "Column21", "Column22", "Column23", "Column24", "Column25", "Column26", "Column27", "Column28", "Column29", "Column30"}, {"Data.Column1", "Data.Column2", "Data.Column3", "Data.Column4", "Data.Column5", "Data.Column6", "Data.Column7", "Data.Column8", "Data.Column9", "Data.Column10", "Data.Column11", "Data.Column12", "Data.Column13", "Data.Column14", "Data.Column15", "Data.Column16", "Data.Column17", "Data.Column18", "Data.Column19", "Data.Column20", "Data.Column21", "Data.Column22", "Data.Column23", "Data.Column24", "Data.Column25", "Data.Column26", "Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30"}),
    #"Added Custom" = Table.AddColumn(#"Expanded Data", "Custom", each Text.Select([Name],{"0".."9"})),
    #"Changed Type" = Table.TransformColumnTypes(#"Added Custom",{{"Custom", Int64.Type}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Custom", "Tháng"}}),
    #"Removed Columns1" = Table.RemoveColumns(#"Renamed Columns",{"Name"}),
    #"Filtered Rows1" = Table.SelectRows(#"Removed Columns1", each ([Data.Column29] = 2) and ([Data.Column28] = "") and ([Data.Column7] <> null)),
    #"Removed Columns2" = Table.RemoveColumns(#"Filtered Rows1",{"Data.Column15", "Data.Column16", "Data.Column17", "Data.Column18", "Data.Column19", "Data.Column20", "Data.Column21", "Data.Column22", "Data.Column23", "Data.Column24", "Data.Column25", "Data.Column26", "Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Removed Columns2",{{"Data.Column1", Int64.Type}}),
    #"Removed Columns3" = Table.RemoveColumns(#"Changed Type1",{"Data.Column8"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns3",{{"Data.Column1", "SPT"}, {"Data.Column2", "N_HD"}, {"Data.Column3", "N_PT"}, {"Data.Column4", "N_NT"}, {"Data.Column5", "Tram"}, {"Data.Column9", "L_100"}, {"Data.Column10", "Ak"}, {"Data.Column11", "Vk"}, {"Data.Column12", "Sk"}, {"Data.Column13", "Qk"}, {"Data.Column14", "L_NT"}}),
    #"Sorted Rows" = Table.Sort(#"Renamed Columns1",{{"Tháng", Order.Ascending}, {"Tram", Order.Ascending}, {"SPT", Order.Ascending}}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Sorted Rows",{{"N_HD", type date}, {"N_PT", type date}, {"N_NT", type date}}),
    #"Added Custom1" = Table.AddColumn(#"Changed Type2", "Merge", each Text.From([SPT]) & "|" & Text.From([Tram])& "|" & Text.From([Tháng])),
    #"Removed Columns4" = Table.RemoveColumns(#"Added Custom1",{"SPT", "N_HD", "N_PT", "N_NT", "Tram", "Data.Column6", "Data.Column7", "L_100", "Ak", "Vk", "Sk", "Qk", "L_NT", "Tháng"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns4"),
    #"Added Index" = Table.AddIndexColumn(#"Removed Duplicates", "Index", 0, 1, Int64.Type),
    #"Inserted Addition" = Table.AddColumn(#"Added Index", "Addition", each [Index] + 1, type number),
    #"Removed Columns5" = Table.RemoveColumns(#"Inserted Addition",{"Index"}),
    #"Renamed Columns2" = Table.RenameColumns(#"Removed Columns5",{{"Addition", "Index"}})
in
    #"Renamed Columns2";

shared #"Tên cám" = let
    data = Excel.CurrentWorkbook(){[Name="forwpath"]}[Content],
    forwpath = data{0}[Column1],
    topath = forwpath & "8. Thủy\Path.xlsx",
    datapath = Excel.Workbook(File.Contents(topath), null, true),
    allpath = datapath{[Item="_2025",Kind="Table"]}[Data],
    backpath = allpath{0}[path],
    FilePath = forwpath & "8. Thủy\KHO NĂM 2025\Tổng hợp NXT các trạm 2025.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    #"Tên cám_Sheet" = Source{[Item="Tên cám",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(#"Tên cám_Sheet",{{"Column1", type text}, {"Column2", type text}, {"Column3", type text}, {"Column4", type text}, {"Column5", type text}}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Changed Type", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers",{{"Than tại NXT", type text}, {"Biểu 8", type text}, {"Biểu 7", type text}, {"TD", type text}, {"Tên TD", type text}})
in
    #"Changed Type1";

shared #"Tồn TN" = let
    Source = Excel.CurrentWorkbook(){[Name="Tồn"]}[Content],
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"SPT", Int64.Type}, {"N_HD", type datetime}, {"N_PT", type datetime}, {"N_NT", type datetime}, {"Tram", type text}, {"Data.Column6", type text}, {"Data.Column7", type text}, {"L_100", type number}, {"Ak", type number}, {"Vk", type number}, {"Sk", type number}, {"Qk", Int64.Type}, {"L_T", type number}, {"STTPA", Int64.Type}, {"Tháng", Int64.Type}, {"C_TP", type text}, {"C_PT", type text}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"L_T", "L_TTN"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each ([Tháng] <> 0))
in
    #"Filtered Rows";

shared HHB = let
    Source = Excel.CurrentWorkbook(){[Name="HHB"]}[Content],
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"SPT", Int64.Type}, {"N_HD", type datetime}, {"N_PT", type datetime}, {"N_NT", type datetime}, {"Tram", type text}, {"Data.Column6", type text}, {"Data.Column7", type text}, {"L_100", type number}, {"Ak", type number}, {"Vk", type number}, {"Sk", type number}, {"Qk", Int64.Type}, {"L_HH", type number}, {"STTPA", Int64.Type}, {"Tháng", Int64.Type}, {"C_TP", type text}, {"C_PT", type text}})
in
    #"Changed Type";

shared HHKK = let
    Source = Excel.CurrentWorkbook(){[Name="HHKK"]}[Content],
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"SPT", type any}, {"N_HD", type any}, {"N_PT", type any}, {"N_NT", type any}, {"Tram", type any}, {"Data.Column6", type any}, {"Data.Column7", type any}, {"L_100", type any}, {"Ak", type any}, {"Vk", type any}, {"Sk", type any}, {"Qk", type any}, {"L_KK", type any}, {"STTPA", type any}, {"Tháng", type any}, {"C_TP", type text}, {"C_PT", type text}})
in
    #"Changed Type";

shared #"Tồn TT" = let
    Source = Excel.CurrentWorkbook(){[Name="Tồn"]}[Content],
    #"Changed Type" = Table.TransformColumnTypes(Source, {{"SPT", Int64.Type}, {"N_HD", type datetime}, {"N_PT", type datetime}, {"N_NT", type datetime}, {"Tram", type text}, {"Data.Column6", type text}, {"Data.Column7", type text}, {"L_100", type number}, {"Ak", type number}, {"Vk", type number}, {"Sk", type number}, {"Qk", Int64.Type}, {"L_T", type number}, {"STTPA", Int64.Type}, {"Tháng", Int64.Type}, {"C_TP", type text}, {"C_PT", type text}}),
    MaxValue = List.Max(#"Changed Type"[Tháng]),
    FilteredTable = Table.SelectRows(#"Changed Type", each[Tháng] <> MaxValue),
    #"Renamed Columns" = Table.RenameColumns(FilteredTable, {{"L_T", "L_TTT"}}),
    #"Added to Column" = Table.TransformColumns(#"Renamed Columns", {{"Tháng", each _ + 1, type number}})
in
    #"Added to Column";

shared #"PA (2)" = let
    Source = Excel.CurrentWorkbook(){[Name="PA"]}[Content]
in
    Source;

shared Bán = let
    Source = Table.Combine({#"Tồn TT", #"PA (2)", HHKK, HHB, #"Tồn TN", XCN, NCN}),
    #"Replaced Value" = Table.ReplaceValue(Source,null,0,Replacer.ReplaceValue,{"L_NT", "L_KK", "L_HH", "L_TTN", "L_XCN", "L_NCN"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value",null,0,Replacer.ReplaceValue,{"L_XCN", "L_NCN"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Replaced Value2",{{"L_NT", type number}, {"L_KK", type number}, {"L_HH", type number}, {"L_TTN", type number}, {"N_NT", type date}, {"N_PT", type date}, {"N_HD", type date}}),
    #"Rounded Off" = Table.TransformColumns(#"Changed Type",{{"L_NT", each Number.Round(_, 2), type number}, {"L_KK", each Number.Round(_, 2), type number}, {"L_HH", each Number.Round(_, 2), type number}, {"L_TTN", each Number.Round(_, 2), type number}, {"L_XCN", each Number.Round(_, 2), type number}, {"L_NCN", each Number.Round(_, 2), type number}}),
    #"Replaced Value1" = Table.ReplaceValue(#"Rounded Off",null,0,Replacer.ReplaceValue,{"L_TTT"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Replaced Value1",{{"L_TTT", type number}}),
    #"Grouped Rows" = Table.Group(#"Changed Type1", {"SPT", "N_HD", "N_PT", "N_NT", "Tram", "Data.Column6", "Data.Column7", "Ak", "Vk", "Sk", "Qk", "STTPA", "Cảng", "Tháng"}, {{"L_TTT", each List.Sum([L_TTT]), type nullable number}, {"L_TTN", each List.Sum([L_TTN]), type number}, {"L_PA", each List.Sum([L_NT]), type number}, {"L_HHB", each List.Sum([L_HH]), type number}, {"L_KK", each List.Sum([L_KK]), type number}, {"L_XCN", each List.Sum([L_XCN]), type number}, {"L_NCN", each List.Sum([L_NCN]), type number}}),
    #"Added Custom" = Table.AddColumn(#"Grouped Rows", "L_B", each [L_TTT]+[L_PA]-[L_HHB]-[L_KK]-[L_TTN]+[L_NCN]-[L_XCN]),
    #"Filtered Rows" = Table.SelectRows(#"Added Custom", each ([Tháng] <> 0) and ([Data.Column7] <> null)),
    #"Rounded Off1" = Table.TransformColumns(#"Filtered Rows",{{"L_B", each Number.Round(_, 2), type number}})
in
    #"Rounded Off1";

shared sheet = let
    Source = Excel.CurrentWorkbook(),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Name] = "'CÁM 6B.1(BOT (T)'!Print_Area" or [Name] = "'CÁM 6B.1(BOT'!Print_Area" or [Name] = "'Giá vốn 6b.1'!Print_Area" or [Name] = "'Giá vốn than trong nước'!Print_Area" or [Name] = "'Quyết toán (T)'!Print_Area" or [Name] = "'Quyết toán'!Print_Area")),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Content"}),
    #"Added Custom" = Table.AddColumn(#"Removed Columns", "Custom", each Text.Split([Name], "'"){1}),
    #"Removed Columns1" = Table.RemoveColumns(#"Added Custom",{"Name"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns1",{{"Custom", "Sheet"}})
in
    #"Renamed Columns";

shared XCN = let
    Source = Excel.CurrentWorkbook(){[Name="CN"]}[Content],
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"SPT", type any}, {"N_HD", type any}, {"N_PT", type any}, {"N_NT", type any}, {"Tram", type any}, {"Data.Column6", type any}, {"Data.Column7", type any}, {"L_100", type any}, {"Ak", type any}, {"Vk", type any}, {"Sk", type any}, {"Qk", type any}, {"L_T", type any}, {"STTPA", type any}, {"Cảng", type any}, {"Tháng", type any}, {"C_TP", Int64.Type}, {"C_PT", type any}, {"PL", Int64.Type}, {"C_B8", type any}, {"C_CN", type any}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each ([Tram] <> null)),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"C_CN"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"L_T", "L_XCN"}})
in
    #"Renamed Columns";

shared NCN = let
    Source = Excel.CurrentWorkbook(){[Name="CN"]}[Content],
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"SPT", type any}, {"N_HD", type any}, {"N_PT", type any}, {"N_NT", type any}, {"Tram", type any}, {"Data.Column6", type any}, {"Data.Column7", type any}, {"L_100", type any}, {"Ak", type any}, {"Vk", type any}, {"Sk", type any}, {"Qk", type any}, {"L_T", type any}, {"STTPA", type any}, {"Cảng", type any}, {"Tháng", type any}, {"C_TP", Int64.Type}, {"C_PT", type any}, {"PL", Int64.Type}, {"C_B8", type any}, {"C_CN", type any}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each ([Tram] <> null)),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Data.Column6"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"C_CN", "Data.Column6"}, {"L_T", "L_NCN"}})
in
    #"Renamed Columns";

shared tenthan = let
    Source = Table.Combine({#"Tồn TT", #"PA (2)", HHKK, HHB, #"Tồn TN", XCN, NCN}),
    #"Replaced Value" = Table.ReplaceValue(Source,null,0,Replacer.ReplaceValue,{"L_NT", "L_KK", "L_HH", "L_TTN", "L_XCN", "L_NCN"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value",null,0,Replacer.ReplaceValue,{"L_XCN", "L_NCN"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Replaced Value2",{{"L_NT", type number}, {"L_KK", type number}, {"L_HH", type number}, {"L_TTN", type number}, {"N_NT", type date}, {"N_PT", type date}, {"N_HD", type date}}),
    #"Rounded Off" = Table.TransformColumns(#"Changed Type",{{"L_NT", each Number.Round(_, 2), type number}, {"L_KK", each Number.Round(_, 2), type number}, {"L_HH", each Number.Round(_, 2), type number}, {"L_TTN", each Number.Round(_, 2), type number}, {"L_XCN", each Number.Round(_, 2), type number}, {"L_NCN", each Number.Round(_, 2), type number}}),
    #"Replaced Value1" = Table.ReplaceValue(#"Rounded Off",null,0,Replacer.ReplaceValue,{"L_TTT"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Replaced Value1",{{"L_TTT", type number}}),
    #"Grouped Rows" = Table.Group(#"Changed Type1", {"SPT", "N_HD", "N_PT", "N_NT", "Tram", "Data.Column6", "Data.Column7", "Ak", "Vk", "Sk", "Qk", "STTPA", "Cảng", "Tháng"}, {{"L_TTT", each List.Sum([L_TTT]), type nullable number}, {"L_TTN", each List.Sum([L_TTN]), type number}, {"L_PA", each List.Sum([L_NT]), type number}, {"L_HHB", each List.Sum([L_HH]), type number}, {"L_KK", each List.Sum([L_KK]), type number}, {"L_XCN", each List.Sum([L_XCN]), type number}, {"L_NCN", each List.Sum([L_NCN]), type number}}),
    #"Added Custom" = Table.AddColumn(#"Grouped Rows", "L_B", each [L_TTT]+[L_PA]-[L_HHB]-[L_KK]-[L_TTN]+[L_NCN]-[L_XCN]),
    #"Filtered Rows" = Table.SelectRows(#"Added Custom", each ([Tháng] <> 0) and ([Data.Column7] <> null)),
    #"Rounded Off1" = Table.TransformColumns(#"Filtered Rows",{{"L_B", each Number.Round(_, 2), type number}}),
    #"Removed Columns" = Table.RemoveColumns(#"Rounded Off1",{"N_PT", "N_NT", "Ak", "Vk", "Sk", "Qk", "Cảng", "L_TTT", "L_TTN", "L_PA", "L_HHB", "L_KK", "L_XCN", "L_NCN"})
in
    #"Removed Columns";