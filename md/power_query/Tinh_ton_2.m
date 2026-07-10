section Section1;

shared HHHB4 = let
    
    Source = Excel.CurrentWorkbook(),
    #"HHB!Print_Area" = Source{[Name="HHB!Print_Area"]}[Content],
    #"Promoted Headers" = Table.PromoteHeaders(#"HHB!Print_Area", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"SPT", type any}, {"N_HD", type any}, {"N_PT", type any}, {"N_NT", type any}, {"Tram", type any}, {"Data.Column6", type any}, {"Data.Column7", type any}, {"L_100", type any}, {"Ak", type any}, {"Vk", type any}, {"Sk", type any}, {"Qk", type any}, {"L_HH", type any}, {"STTPA", type any}, {"Tháng", type any}, {"C_TP", type any}, {"C_PT", type any}}),
    #"Removed Errors" = Table.RemoveRowsWithErrors(#"Changed Type", {"SPT"}),
    #"Removed Errors1" = Table.RemoveRowsWithErrors(#"Removed Errors", {"C_PT"}),
    #"Removed Blank Rows" = Table.SelectRows(#"Removed Errors1", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Filtered Rows" = Table.SelectRows(#"Removed Blank Rows", each ([Data.Column7] <> 0))
in
    #"Filtered Rows";

shared HHKK5 = let
    Source = Excel.CurrentWorkbook(),
    #"HHKK!Print_Area" = Source{[Name="HHKK!Print_Area"]}[Content],
    #"Promoted Headers" = Table.PromoteHeaders(#"HHKK!Print_Area", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"SPT", type any}, {"N_HD", type any}, {"N_PT", type any}, {"N_NT", type any}, {"Tram", type any}, {"Data.Column6", type any}, {"Data.Column7", type any}, {"L_100", type any}, {"Ak", type any}, {"Vk", type any}, {"Sk", type any}, {"Qk", type any}, {"L_KK", type any}, {"STTPA", type any}, {"Tháng", type any}, {"C_TP", type any}, {"C_PT", type any}}),
    #"Removed Errors" = Table.RemoveRowsWithErrors(#"Changed Type", {"C_PT"}),
    #"Removed Blank Rows" = Table.SelectRows(#"Removed Errors", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Filtered Rows" = Table.SelectRows(#"Removed Blank Rows", each ([Data.Column7] <> 0))
in
    #"Filtered Rows";

shared PA2 = let
    
    Source = Excel.CurrentWorkbook(),
    #"PA!Print_Area" = Source{[Name="PA!Print_Area"]}[Content],
    #"Promoted Headers" = Table.PromoteHeaders(#"PA!Print_Area", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"SPT", Int64.Type}, {"N_HD", type date}, {"N_PT", type date}, {"N_NT", type date}, {"Tram", type text}, {"Data.Column6", type text}, {"Data.Column7", type text}, {"L_100", type number}, {"Ak", type number}, {"Vk", type number}, {"Sk", type number}, {"Qk", Int64.Type}, {"L_NT", type number}, {"STTPA", Int64.Type}, {"Tháng", Int64.Type}, {"C_TP", type text}, {"C_PT", type text}}),
    #"Removed Blank Rows" = Table.SelectRows(#"Changed Type", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null})))
in
    #"Removed Blank Rows";

shared Tồn = let
    
    Source = Excel.CurrentWorkbook(),
    #"Tồn!Print_Area" = Source{[Name="Tồn!Print_Area"]}[Content],
    #"Promoted Headers" = Table.PromoteHeaders(#"Tồn!Print_Area", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"SPT", Int64.Type}, {"N_HD", type date}, {"N_PT", type date}, {"N_NT", type date}, {"Tram", type text}, {"Data.Column6", type text}, {"Data.Column7", type text}, {"L_100", type number}, {"Ak", type number}, {"Vk", type number}, {"Sk", type number}, {"Qk", Int64.Type}, {"L_T", type number}, {"STTPA", Int64.Type}, {"Tháng", Int64.Type}, {"C_TP", type text}, {"C_PT", type text}}),
    #"Filtered Rows" = Table.SelectRows(#"Changed Type", each [Tháng] > 0),
    #"Removed Blank Rows" = Table.SelectRows(#"Filtered Rows", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null})))
in
    #"Removed Blank Rows";

shared TồnTT = let
    
    Source = Excel.CurrentWorkbook(),
    #"Tồn!Print_Area" = Source{[Name="Tồn!Print_Area"]}[Content],
    #"Promoted Headers" = Table.PromoteHeaders(#"Tồn!Print_Area", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"SPT", Int64.Type}, {"N_HD", type date}, {"N_PT", type date}, {"N_NT", type date}, {"Tram", type text}, {"Data.Column6", type text}, {"Data.Column7", type text}, {"L_100", type number}, {"Ak", type number}, {"Vk", type number}, {"Sk", type number}, {"Qk", Int64.Type}, {"L_T", type number}, {"STTPA", Int64.Type}, {"Tháng", Int64.Type}, {"C_TP", type text}, {"C_PT", type text}}),
    MaxValue = List.Max(PA2[Tháng]),
    FilteredTable = Table.SelectRows(#"Changed Type", each[Tháng] <> MaxValue),
    #"Added to Column" = Table.TransformColumns(FilteredTable, {{"Tháng", each _ + 1, type number}}),
    #"Renamed Columns" = Table.RenameColumns(#"Added to Column",{{"L_T", "L_TT"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns", each [Tháng] < 13),
    #"Removed Blank Rows" = Table.SelectRows(#"Filtered Rows", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null})))
in
    #"Removed Blank Rows";

shared XCN = let
    
    Source = Excel.CurrentWorkbook(),
    #"PA!Print_Area" = Source{[Name="XCN!Print_Area"]}[Content],
    #"Promoted Headers" = Table.PromoteHeaders(#"PA!Print_Area", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"SPT", Int64.Type}, {"N_HD", type date}, {"N_PT", type date}, {"N_NT", type date}, {"Tram", type text}, {"Data.Column6", type text}, {"Data.Column7", type text}, {"L_100", type number}, {"Ak", type number}, {"Vk", type number}, {"Sk", type number}, {"Qk", Int64.Type}, {"L_T", type number}, {"STTPA", Int64.Type}, {"Tháng", Int64.Type}, {"C_TP", type text}, {"C_PT", type text}}),
    #"Removed Blank Rows" = Table.SelectRows(#"Changed Type", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Blank Rows",{{"L_T", "L_XCN"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"C_CN"}),
    #"Filtered Rows" = Table.SelectRows(#"Removed Columns", each ([Data.Column7] <> "0"))
in
    #"Filtered Rows";

shared NCN = let
    
    Source = Excel.CurrentWorkbook(),
    #"PA!Print_Area" = Source{[Name="XCN!Print_Area"]}[Content],
    #"Promoted Headers" = Table.PromoteHeaders(#"PA!Print_Area", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"SPT", Int64.Type}, {"N_HD", type date}, {"N_PT", type date}, {"N_NT", type date}, {"Tram", type text}, {"Data.Column6", type text}, {"Data.Column7", type text}, {"L_100", type number}, {"Ak", type number}, {"Vk", type number}, {"Sk", type number}, {"Qk", Int64.Type}, {"L_T", type number}, {"STTPA", Int64.Type}, {"Tháng", Int64.Type}, {"C_TP", type text}, {"C_PT", type text}}),
    #"Removed Blank Rows" = Table.SelectRows(#"Changed Type", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Blank Rows",{{"L_T", "L_NCN"}}),
    #"Removed Columns" = Table.RemoveColumns(#"Renamed Columns",{"Data.Column6"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns",{{"C_CN", "Data.Column6"}}),
    #"Filtered Rows" = Table.SelectRows(#"Renamed Columns1", each ([L_100] <> 0))
in
    #"Filtered Rows";

shared Append1 = let
    Source = Table.Combine({PA2, TồnTT, Tồn, HHHB4, HHKK5, XCN, NCN}),
    #"Rounded Off" = Table.TransformColumns(Source,{{"L_NT", each Number.Round(_, 2), type number}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Rounded Off",{{"L_TT", type number}, {"L_T", type number}, {"L_HH", type number}, {"L_KK", type number}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type",null,0,Replacer.ReplaceValue,{"L_TT", "L_T", "L_HH", "L_KK","L_XCN","L_NCN"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",null,0,Replacer.ReplaceValue,{"L_NT"}),
    #"Rounded Off1" = Table.TransformColumns(#"Replaced Value1",{{"L_TT", each Number.Round(_, 2), type number}, {"L_T", each Number.Round(_, 2), type number}, {"L_HH", each Number.Round(_, 2), type number}, {"L_KK", each Number.Round(_, 2), type number}, {"L_XCN", each Number.Round(_, 2), type number}, {"L_NCN", each Number.Round(_, 2), type number}}),
    #"Added Custom" = Table.AddColumn(#"Rounded Off1", "Custom", each [L_TT]+[L_NT]-[L_T]-[L_HH]-[L_KK]-[L_XCN]+[L_NCN]),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom",{{"Custom", "L_B"}}),
    #"Grouped Rows" = Table.Group(#"Renamed Columns", {"SPT", "Tram", "Data.Column6", "Tháng", "STTPA"}, {{"L_B", each List.Sum([L_B]), type number}}),
    #"Rounded Off2" = Table.TransformColumns(#"Grouped Rows",{{"L_B", each Number.Round(_, 2), type number}}),
    #"Sorted Rows" = Table.Sort(#"Rounded Off2",{{"Tháng", Order.Descending}, {"STTPA", Order.Descending}})
in
    #"Sorted Rows";

shared Table3 = let
    Source = Excel.CurrentWorkbook(){[Name="Table3"]}[Content],
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Tháng", Int64.Type}, {"Tram", type text}, {"Cam_TP", type text}, {"Ton", type number}, {"KK", type number}, {"HHB", type number}})
in
    #"Changed Type";

shared Append2 = let
    Source = Table.Combine({PA2, TồnTT, Tồn, HHHB4, HHKK5, XCN, NCN}),
    #"Rounded Off" = Table.TransformColumns(Source,{{"L_NT", each Number.Round(_, 2), type number}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Rounded Off",{{"L_TT", type number}, {"L_T", type number}, {"L_HH", type number}, {"L_KK", type number}, {"L_XCN", type number}, {"L_NCN", type number}, {"N_HD", type date}, {"N_PT", type date}, {"N_NT", type date}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type",null,0,Replacer.ReplaceValue,{"L_TT", "L_T", "L_HH", "L_KK", "L_XCN", "L_NCN"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",null,0,Replacer.ReplaceValue,{"L_NT"}),
    #"Rounded Off1" = Table.TransformColumns(#"Replaced Value1",{{"L_TT", each Number.Round(_, 2), type number}, {"L_T", each Number.Round(_, 2), type number}, {"L_HH", each Number.Round(_, 2), type number}, {"L_KK", each Number.Round(_, 2), type number}, {"L_XCN", each Number.Round(_, 2), type number}, {"L_NCN", each Number.Round(_, 2), type number}}),
    #"Added Custom" = Table.AddColumn(#"Rounded Off1", "Custom", each [L_TT]+[L_NT]-[L_T]-[L_HH]-[L_KK]+[L_NCN]-[L_XCN]),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom",{{"Custom", "L_B"}}),
    #"Grouped Rows" = Table.Group(#"Renamed Columns", {"SPT", "N_HD", "N_PT", "N_NT", "Tram", "Data.Column6", "Data.Column7", "Ak", "Vk", "Sk", "Qk", "STTPA", "Cảng", "Tháng"}, {{"L_B", each List.Sum([L_B]), type number}}),
    #"Sorted Rows" = Table.Sort(#"Grouped Rows",{{"Tram", Order.Ascending}, {"Data.Column6", Order.Ascending}, {"STTPA", Order.Descending}, {"Tháng", Order.Descending}})
in
    #"Sorted Rows";

shared PA = let
    
    Source = Excel.CurrentWorkbook(),
    #"PA!Print_Area" = Source{[Name="PA!Print_Area"]}[Content],
    #"Promoted Headers" = Table.PromoteHeaders(#"PA!Print_Area", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"SPT", Int64.Type}, {"N_HD", type date}, {"N_PT", type date}, {"N_NT", type date}, {"Tram", type text}, {"Data.Column6", type text}, {"Data.Column7", type text}, {"L_100", type number}, {"Ak", type number}, {"Vk", type number}, {"Sk", type number}, {"Qk", Int64.Type}, {"L_NT", type number}, {"STTPA", Int64.Type}, {"Tháng", Int64.Type}, {"C_TP", type text}, {"C_PT", type text}}),
    #"Removed Columns" = Table.RemoveColumns(#"Changed Type",{"N_HD", "N_PT", "N_NT", "Data.Column6", "Data.Column7", "L_100", "Ak", "Vk", "Sk", "Qk", "L_NT", "C_PT", "PL", "C_B8"}),
    #"Removed Duplicates" = Table.Distinct(#"Removed Columns")
in
    #"Removed Duplicates";

shared Check = let
    Source = Table.Combine({PA2, TồnTT, Tồn, HHHB4, HHKK5, XCN, NCN}),
    #"Rounded Off" = Table.TransformColumns(Source,{{"L_NT", each Number.Round(_, 2), type number}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Rounded Off",{{"L_TT", type number}, {"L_T", type number}, {"L_HH", type number}, {"L_KK", type number}, {"N_HD", type date}, {"N_PT", type date}, {"N_NT", type date}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type",null,0,Replacer.ReplaceValue,{"L_TT", "L_T", "L_HH", "L_KK", "L_XCN", "L_NCN"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",null,0,Replacer.ReplaceValue,{"L_NT"}),
    #"Rounded Off1" = Table.TransformColumns(#"Replaced Value1",{{"L_TT", each Number.Round(_, 2), type number}, {"L_T", each Number.Round(_, 2), type number}, {"L_HH", each Number.Round(_, 2), type number}, {"L_KK", each Number.Round(_, 2), type number}}),
    #"Added Custom" = Table.AddColumn(#"Rounded Off1", "Custom", each [L_TT]+[L_NT]-[L_T]-[L_HH]-[L_KK]+[L_NCN]-[L_XCN]),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom",{{"Custom", "L_B"}}),
    #"Grouped Rows" = Table.Group(#"Renamed Columns", {"SPT", "N_HD", "N_PT", "N_NT", "Tram", "Data.Column6", "Ak", "Vk", "Sk", "Qk", "STTPA", "Cảng", "Tháng"}, {{"L_B", each List.Sum([L_B]), type number}, {"L_TT", each List.Sum([L_TT]), type number}, {"L_T", each List.Sum([L_T]), type number}, {"L_HH", each List.Sum([L_HH]), type number}, {"L_KK", each List.Sum([L_KK]), type number}, {"L_XCN", each List.Sum([L_XCN]), type nullable number}, {"L_NCN", each List.Sum([L_NCN]), type nullable number}}),
    #"Sorted Rows" = Table.Sort(#"Grouped Rows",{{"Tháng", Order.Descending}, {"STTPA", Order.Descending}})
in
    #"Sorted Rows";

shared C2 = let
    Source = Table.Combine({PA2, TồnTT, Tồn, HHHB4, HHKK5}),
    #"Rounded Off" = Table.TransformColumns(Source,{{"L_NT", each Number.Round(_, 2), type number}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Rounded Off",{{"L_TT", type number}, {"L_T", type number}, {"L_HH", type number}, {"L_KK", type number}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type",null,0,Replacer.ReplaceValue,{"L_TT", "L_T", "L_HH", "L_KK"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value",null,0,Replacer.ReplaceValue,{"L_NT"}),
    #"Rounded Off1" = Table.TransformColumns(#"Replaced Value1",{{"L_TT", each Number.Round(_, 2), type number}, {"L_T", each Number.Round(_, 2), type number}, {"L_HH", each Number.Round(_, 2), type number}, {"L_KK", each Number.Round(_, 2), type number}}),
    #"Added Custom" = Table.AddColumn(#"Rounded Off1", "Custom", each [L_TT]+[L_NT]-[L_T]-[L_HH]-[L_KK]),
    #"Renamed Columns" = Table.RenameColumns(#"Added Custom",{{"Custom", "L_B"}}),
    #"Grouped Rows" = Table.Group(#"Renamed Columns", {"SPT", "N_HD", "N_PT", "N_NT", "Tram", "Data.Column6", "Data.Column7", "Ak", "Vk", "Sk", "Qk", "STTPA", "Cảng", "Tháng"}, {{"L_B", each List.Sum([L_B]), type number}}),
    #"Sorted Rows" = Table.Sort(#"Grouped Rows",{{"Tháng", Order.Descending}, {"STTPA", Order.Descending}}),
    #"Removed Columns" = Table.RemoveColumns(#"Sorted Rows",{"N_HD", "Data.Column7", "Ak", "Vk", "Sk", "Qk", "Cảng"}),
    #"Grouped Rows1" = Table.Group(#"Removed Columns", {"SPT", "Tram", "Data.Column6", "N_NT", "Tháng", "STTPA"}, {{"Luong", each List.Sum([L_B]), type number}}),
    #"Sorted Rows1" = Table.Sort(#"Grouped Rows1",{{"Tram", Order.Ascending}}),
    #"Removed Blank Rows" = Table.SelectRows(#"Sorted Rows1", each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    #"Filtered Rows" = Table.SelectRows(#"Removed Blank Rows", each ([Tram] <> null)),
    #"Sorted Rows2" = Table.Sort(#"Filtered Rows",{{"Tram", Order.Ascending}, {"Data.Column6", Order.Ascending}, {"N_NT", Order.Descending}})
in
    #"Sorted Rows2";