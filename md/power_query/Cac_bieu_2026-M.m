section Section1;

shared NXT = let
    data = Excel.CurrentWorkbook(){[Name="Table4"]}[Content],
    forwpath = data{0}[Column1],
    topath = forwpath & "Thủy\Path.xlsx",
    datapath = Excel.Workbook(File.Contents(topath), null, true),
    allpath = datapath{[Item="_2025",Kind="Table"]}[Data],
    backpath = allpath{0}[path],
    FilePath = forwpath & "Thủy\KHO NĂM 2026\Tổng hợp NXT các trạm 2026.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    #"Thang 7 2023_Sheet" = Source{[Item="2026",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(#"Thang 7 2023_Sheet", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Tồn đầu kỳ", type number}, {"Column4", type number}, {"Nhập mua", type number}, {"Column6", type number}, {"Column7", type number}, {"Nhập chế biến", type number}, {"Column9", type number}, {"Column10", type number}, {"Nhập pha trộn", type number}, {"Column12", type number}, {"Column13", type number}, {"Tổng nhập CB", type number}, {"Column15", type number}, {"Column16", type number}, {"Chiết khấu than#(lf) thương mại", type number}, {"Nhập thừa kiểm kê", type number}, {"Column19", type number}, {"Nhập khác", type number}, {"Column21", type number}, {"Nhập nội bộ", type number}, {"Column23", type number}, {"Tổng nhập trong kỳ", type number}, {"Column25", type number}, {"Chiết khấu than#(lf) thương mại_1", type number}, {"Xuất bán ", type number}, {"Column28", type number}, {"C.khấu than VD", type number}, {"Hàng đi đường tháng trước nhập kho", type number}, {"Column31", type number}, {"Xuất bán nội bộ MB", type number}, {"Column33", type number}, {"Xuất hao hụt hàng bán", type number}, {"Column35", type number}, {"Xuất chuyển ẩm", type number}, {"Column37", type number}, {"Xuất pha trộn", type number}, {"Column39", type number}, {"Xuất chế biến", type number}, {"Column41", type number}, {"Tổng xuất CB", type number}, {"Column43", type number}, {"Xuất thiếu kiểm kê", type number}, {"Column45", type number}, {"Xuất khác", type number}, {"Column47", type number}, {"Tổng xuất", type number}, {"Column49", type number}, {"Tồn trong kho", type number}, {"Column51", type number}, {"Đi đường", type number}, {"Column53", type number}, {"Gửi bán", type number}, {"Column55", type number}}),
    #"Replaced Value" = Table.ReplaceValue(#"Changed Type",null,0,Replacer.ReplaceValue,{"Tồn đầu kỳ", "Column4", "Nhập mua", "Column6", "Column7", "Nhập chế biến", "Column9", "Column10", "Nhập pha trộn", "Column12", "Column13", "Tổng nhập CB", "Column15", "Column16", "Chiết khấu than#(lf) thương mại", "Nhập thừa kiểm kê", "Column19", "Nhập khác", "Column21", "Nhập nội bộ", "Column23", "Tổng nhập trong kỳ", "Column25", "Chiết khấu than#(lf) thương mại_1", "Xuất bán ", "Column28", "C.khấu than VD", "Hàng đi đường tháng trước nhập kho", "Column31", "Xuất bán nội bộ MB", "Column33", "Xuất hao hụt hàng bán", "Column35", "Xuất chuyển ẩm", "Column37", "Xuất pha trộn", "Column39", "Xuất chế biến", "Column41", "Tổng xuất CB", "Column43", "Xuất thiếu kiểm kê", "Column45", "Xuất khác", "Column47", "Tổng xuất", "Column49", "Tồn trong kho", "Column51", "Đi đường", "Column53", "Gửi bán", "Column55"}),
    #"Replaced Errors" = Table.ReplaceErrorValues(#"Replaced Value", {{"Tồn đầu kỳ", 0}, {"Column4", 0}, {"Nhập mua", 0}, {"Column6", 0}, {"Column7", 0}, {"Nhập chế biến", 0}, {"Column9", 0}, {"Column10", 0}, {"Nhập pha trộn", 0}, {"Column12", 0}, {"Column13", 0}, {"Tổng nhập CB", 0}, {"Column15", 0}, {"Column16", 0}, {"Chiết khấu than#(lf) thương mại", 0}, {"Nhập thừa kiểm kê", 0}, {"Column19", 0}, {"Nhập khác", 0}, {"Column21", 0}, {"Nhập nội bộ", 0}, {"Column23", 0}, {"Tổng nhập trong kỳ", 0}, {"Column25", 0}, {"Chiết khấu than#(lf) thương mại_1", 0}, {"Xuất bán ", 0}, {"Column28", 0}, {"C.khấu than VD", 0}, {"Hàng đi đường tháng trước nhập kho", 0}, {"Column31", 0}, {"Xuất bán nội bộ MB", 0}, {"Column33", 0}, {"Xuất hao hụt hàng bán", 0}, {"Column35", 0}, {"Xuất chuyển ẩm", 0}, {"Column37", 0}, {"Xuất pha trộn", 0}, {"Column39", 0}, {"Xuất chế biến", 0}, {"Column41", 0}, {"Tổng xuất CB", 0}, {"Column43", 0}, {"Xuất thiếu kiểm kê", 0}, {"Column45", 0}, {"Xuất khác", 0}, {"Column47", 0}, {"Tổng xuất", 0}, {"Column49", 0}, {"Tồn trong kho", 0}, {"Column51", 0}, {"Đi đường", 0}, {"Column53", 0}, {"Gửi bán", 0}, {"Column55", 0}}),
    #"Inserted Sum" = Table.AddColumn(#"Replaced Errors", "Addition", each List.Sum({[Tồn đầu kỳ], [Column4], [Nhập mua], [Column6], [Column7], [Nhập chế biến], [Column9], [Column10], [Nhập pha trộn], [Column12], [Column13], [Tổng nhập CB], [Column15], [Column16], [#"Chiết khấu than#(lf) thương mại"], [Nhập thừa kiểm kê], [Column19], [Nhập khác], [Column21], [Nhập nội bộ], [Column23], [Tổng nhập trong kỳ], [Column25], [#"Chiết khấu than#(lf) thương mại_1"], [#"Xuất bán "], [Column28], [C.khấu than VD], [Hàng đi đường tháng trước nhập kho], [Column31], [Xuất bán nội bộ MB], [Column33], [Xuất hao hụt hàng bán], [Column35], [Xuất chuyển ẩm], [Column37], [Xuất pha trộn], [Column39], [Xuất chế biến], [Column41], [Tổng xuất CB], [Column43], [Xuất thiếu kiểm kê], [Column45], [Xuất khác], [Column47], [Tổng xuất], [Column49], [Tồn trong kho], [Column51], [Đi đường], [Column53], [Gửi bán], [Column55]}), type number),
    #"Filtered Rows" = Table.SelectRows(#"Inserted Sum", each ([Addition] <> 0) and ([BM8] <> "-"))
in
    #"Filtered Rows";

shared #"Tên cám" = let
    data = Excel.CurrentWorkbook(){[Name="Table4"]}[Content],
    forwpath = data{0}[Column1],
    topath = forwpath & "Thủy\Path.xlsx",
    datapath = Excel.Workbook(File.Contents(topath), null, true),
    allpath = datapath{[Item="_2025",Kind="Table"]}[Data],
    backpath = allpath{0}[path],
    FilePath = forwpath & "Thủy\KHO NĂM 2026\Tổng hợp NXT các trạm 2026.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    #"Tên cám_Sheet" = Source{[Item="Tên cám",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(#"Tên cám_Sheet",{{"Column1", type text}, {"Column2", type text}, {"Column3", type text}, {"Column4", type text}, {"Column5", type text}}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Changed Type", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers",{{"Than tại NXT", type text}, {"Biểu 8", type text}, {"Biểu 7", type text}, {"TD", type text}, {"Tên TD", type text}})
in
    #"Changed Type1";

shared #"NXT than PTCB" = let
    data = Excel.CurrentWorkbook(){[Name="Table4"]}[Content],
    forwpath = data{0}[Column1],
    FilePath = forwpath & "Thủy\KHO NĂM 2026\THỐNG KÊ\Báo cáo NXT TD-CB (tháng)-print.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Name] = "PT0" or [Name] = "PT1" or [Name] = "PT2" or [Name] = "PT3" or [Name] = "PT4" or [Name] = "PT5" or [Name] = "PT6" or [Name] = "PT7" or [Name] = "PT8" or [Name] = "PT9" or [Name] = "PT10" or [Name] = "PT11" or [Name] = "PT12")),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Item", "Kind", "Hidden"}),
    #"Expanded Data" = Table.ExpandTableColumn(#"Removed Columns", "Data", {"Column1", "Column2", "Column3", "Column4", "Column5", "Column6", "Column7", "Column8", "Column9", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15", "Column16", "Column17", "Column18", "Column19", "Column20", "Column21", "Column22", "Column23", "Column24", "Column25", "Column26", "Column27", "Column28", "Column29", "Column30", "Column31", "Column32", "Column33", "Column34", "Column35", "Column36", "Column37", "Column38", "Column39", "Column40", "Column41", "Column42", "Column43", "Column44"}, {"Data.Column1", "Data.Column2", "Data.Column3", "Data.Column4", "Data.Column5", "Data.Column6", "Data.Column7", "Data.Column8", "Data.Column9", "Data.Column10", "Data.Column11", "Data.Column12", "Data.Column13", "Data.Column14", "Data.Column15", "Data.Column16", "Data.Column17", "Data.Column18", "Data.Column19", "Data.Column20", "Data.Column21", "Data.Column22", "Data.Column23", "Data.Column24", "Data.Column25", "Data.Column26", "Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30", "Data.Column31", "Data.Column32", "Data.Column33", "Data.Column34", "Data.Column35", "Data.Column36", "Data.Column37", "Data.Column38", "Data.Column39", "Data.Column40", "Data.Column41", "Data.Column42", "Data.Column43", "Data.Column44"}),
    #"Removed Columns1" = Table.RemoveColumns(#"Expanded Data",{"Data.Column1", "Data.Column3", "Data.Column4", "Data.Column5", "Data.Column6", "Data.Column7", "Data.Column8", "Data.Column9", "Data.Column10", "Data.Column11", "Data.Column12", "Data.Column13", "Data.Column14", "Data.Column15", "Data.Column16", "Data.Column17", "Data.Column18", "Data.Column19", "Data.Column20", "Data.Column21", "Data.Column22", "Data.Column23", "Data.Column24", "Data.Column25", "Data.Column26", "Data.Column31", "Data.Column32", "Data.Column33", "Data.Column34", "Data.Column35", "Data.Column36", "Data.Column37", "Data.Column38", "Data.Column39", "Data.Column40", "Data.Column41", "Data.Column42", "Data.Column43", "Data.Column44"}),
    #"Added Custom" = Table.AddColumn(#"Removed Columns1", "Tháng", each Text.Select([Name],{"0".."9"})),
    #"Reordered Columns" = Table.ReorderColumns(#"Added Custom",{"Name", "Tháng", "Data.Column2", "Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30"}),
    #"Removed Columns2" = Table.RemoveColumns(#"Reordered Columns",{"Name"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Columns2",{{"Tháng", Int64.Type}}),
    #"Filtered Rows1" = Table.SelectRows(#"Changed Type", each ([Data.Column2] <> null and [Data.Column2] <> 0 and [Data.Column2] <> " - " and [Data.Column2] <> " -  " and [Data.Column2] <> " -Than bùn khác  " and [Data.Column2] <> " Than bùn " and [Data.Column2] <> " Than cám " and [Data.Column2] <> " Than TCVN" and [Data.Column2] <> "Cám độ tro cao " and [Data.Column2] <> "SP NGOÀI TC THAN" and [Data.Column2] <> "Than bùn" and [Data.Column2] <> "Than cám" and [Data.Column2] <> "Than cám Canada" and [Data.Column2] <> "Than cám Mozambique" and [Data.Column2] <> "Than cám Nam Phi" and [Data.Column2] <> "Than cám PTNK" and [Data.Column2] <> "Than cám Úc" and [Data.Column2] <> "Than cục" and [Data.Column2] <> "Than Lào" and [Data.Column2] <> "Than nhập khẩu" and [Data.Column2] <> "Than NK khác" and [Data.Column2] <> "THAN SẠCH THÀNH PHẨM" and [Data.Column2] <> "Than TCCS" and [Data.Column2] <> "Tên sản phẩm") and ([Data.Column27] <> null)),
    #"Replaced Value" = Table.ReplaceValue(#"Filtered Rows1",null,0,Replacer.ReplaceValue,{"Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30"}),
    #"Rounded Off1" = Table.TransformColumns(#"Replaced Value",{{"Data.Column27", each Number.Round(_, 2), type number}, {"Data.Column28", each Number.Round(_, 2), type number}, {"Data.Column29", each Number.Round(_, 2), type number}, {"Data.Column30", each Number.Round(_, 2), type number}}),
    #"Filtered Rows3" = Table.SelectRows(#"Rounded Off1", each ([Data.Column27] <> 0)),
    #"Filtered Rows2" = Table.SelectRows(#"Filtered Rows3", each ([Data.Column27] <> 0 and [Data.Column27] <> "Xuất thiếu kiểm kê")),
    #"Rounded Off" = Table.TransformColumns(#"Filtered Rows2",{{"Data.Column27", each Number.Round(_, 2), type number}, {"Data.Column28", each Number.Round(_, 2), type number}, {"Data.Column29", each Number.Round(_, 2), type number}, {"Data.Column30", each Number.Round(_, 2), type number}}),
    #"Renamed Columns" = Table.RenameColumns(#"Rounded Off",{{"Data.Column2", "Danh mục"}, {"Data.Column28", "Tồn trong kho"}, {"Data.Column29", "Tồn đi đường"}}),
    #"Removed Columns3" = Table.RemoveColumns(#"Renamed Columns",{"Data.Column30"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns3",{{"Tháng", "Thang"}}),
    #"Removed Columns4" = Table.RemoveColumns(#"Renamed Columns1",{"Data.Column27"})
in
    #"Removed Columns4";

shared #"NXT than tự doanh" = let
    data = Excel.CurrentWorkbook(){[Name="Table4"]}[Content],
    forwpath = data{0}[Column1],
    topath = forwpath & "Thủy\Path.xlsx",
    datapath = Excel.Workbook(File.Contents(topath), null, true),
    allpath = datapath{[Item="_2025",Kind="Table"]}[Data],
    backpath = allpath{4}[path],
    FilePath = forwpath & "Thủy\KHO NĂM 2026\THỐNG KÊ\Báo cáo NXT TD-CB (tháng)-print.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Name] = "TD0" or [Name] = "TD1" or [Name] = "TD2" or [Name] = "TD3" or [Name] = "TD4" or [Name] = "TD5" or [Name] = "TD6" or [Name] = "TD7" or [Name] = "TD8" or [Name] = "TD9" or [Name] = "TD10" or [Name] = "TD11" or [Name] = "TD12")),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Item", "Kind", "Hidden"}),
    #"Expanded Data" = Table.ExpandTableColumn(#"Removed Columns", "Data", {"Column1", "Column2", "Column3", "Column4", "Column5", "Column6", "Column7", "Column8", "Column9", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15", "Column16", "Column17", "Column18", "Column19", "Column20", "Column21", "Column22", "Column23", "Column24", "Column25", "Column26", "Column27", "Column28", "Column29", "Column30", "Column31", "Column32", "Column33", "Column34", "Column35", "Column36", "Column37", "Column38", "Column39", "Column40", "Column41", "Column42", "Column43", "Column44"}, {"Data.Column1", "Data.Column2", "Data.Column3", "Data.Column4", "Data.Column5", "Data.Column6", "Data.Column7", "Data.Column8", "Data.Column9", "Data.Column10", "Data.Column11", "Data.Column12", "Data.Column13", "Data.Column14", "Data.Column15", "Data.Column16", "Data.Column17", "Data.Column18", "Data.Column19", "Data.Column20", "Data.Column21", "Data.Column22", "Data.Column23", "Data.Column24", "Data.Column25", "Data.Column26", "Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30", "Data.Column31", "Data.Column32", "Data.Column33", "Data.Column34", "Data.Column35", "Data.Column36", "Data.Column37", "Data.Column38", "Data.Column39", "Data.Column40", "Data.Column41", "Data.Column42", "Data.Column43", "Data.Column44"}),
    #"Removed Columns1" = Table.RemoveColumns(#"Expanded Data",{"Data.Column1", "Data.Column3", "Data.Column4", "Data.Column5", "Data.Column6", "Data.Column7", "Data.Column8", "Data.Column9", "Data.Column10", "Data.Column11", "Data.Column12", "Data.Column13", "Data.Column14", "Data.Column15", "Data.Column16", "Data.Column17", "Data.Column18", "Data.Column19", "Data.Column20", "Data.Column21", "Data.Column22", "Data.Column23", "Data.Column24", "Data.Column25", "Data.Column26", "Data.Column31", "Data.Column32", "Data.Column33", "Data.Column34", "Data.Column35", "Data.Column36", "Data.Column37", "Data.Column38", "Data.Column39", "Data.Column40", "Data.Column41", "Data.Column42", "Data.Column43", "Data.Column44"}),
    #"Added Custom" = Table.AddColumn(#"Removed Columns1", "Tháng", each Text.Select([Name],{"0".."9"})),
    #"Reordered Columns" = Table.ReorderColumns(#"Added Custom",{"Name", "Tháng", "Data.Column2", "Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30"}),
    #"Removed Columns2" = Table.RemoveColumns(#"Reordered Columns",{"Name"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Columns2",{{"Tháng", Int64.Type}}),
    #"Filtered Rows1" = Table.SelectRows(#"Changed Type", each ([Data.Column27] <> null) and ([Data.Column28] <> null) and ([Data.Column2] <> null and [Data.Column2] <> 0 and [Data.Column2] <> " - " and [Data.Column2] <> " -  " and [Data.Column2] <> " -Than bùn khác  " and [Data.Column2] <> " Than bùn " and [Data.Column2] <> " Than cám " and [Data.Column2] <> " Than TCVN" and [Data.Column2] <> "Cám độ tro cao " and [Data.Column2] <> "SP NGOÀI TC THAN" and [Data.Column2] <> "Than bùn" and [Data.Column2] <> "Than cám" and [Data.Column2] <> "Than cám Canada" and [Data.Column2] <> "Than cám Mozambique" and [Data.Column2] <> "Than cám Nam Phi" and [Data.Column2] <> "Than cám PTNK" and [Data.Column2] <> "Than cám Úc" and [Data.Column2] <> "Than cục" and [Data.Column2] <> "Than Lào" and [Data.Column2] <> "Than nhập khẩu" and [Data.Column2] <> "Than NK khác" and [Data.Column2] <> "THAN SẠCH THÀNH PHẨM" and [Data.Column2] <> "Than TCCS" and [Data.Column2] <> "Đất đá lẫn than bùn ( AKTB:    )" and [Data.Column2] <> "Đất đá lẫn than: ( AKTB:    )")),
    #"Replaced Value" = Table.ReplaceValue(#"Filtered Rows1",null,0,Replacer.ReplaceValue,{"Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30"}),
    #"Rounded Off1" = Table.TransformColumns(#"Replaced Value",{{"Data.Column27", each Number.Round(_, 2), type number}, {"Data.Column28", each Number.Round(_, 2), type number}, {"Data.Column29", each Number.Round(_, 2), type number}, {"Data.Column30", each Number.Round(_, 2), type number}}),
    #"Filtered Rows3" = Table.SelectRows(#"Rounded Off1", each ([Data.Column27] <> 0)),
    #"Renamed Columns" = Table.RenameColumns(#"Filtered Rows3",{{"Data.Column2", "Danh mục"}, {"Data.Column28", "Tồn trong kho"}, {"Data.Column29", "Tồn đi đường1"}, {"Data.Column30", "Tồn đi đường"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns",{{"Data.Column27", type number}, {"Tồn trong kho", type number}, {"Tồn đi đường1", type number}, {"Tồn đi đường", type number}}),
    #"Replaced Errors" = Table.ReplaceErrorValues(#"Changed Type1", {{"Data.Column27", 0}, {"Tồn trong kho", 0}, {"Tồn đi đường1", 0}, {"Tồn đi đường", 0}}),
    #"Rounded Off" = Table.TransformColumns(#"Replaced Errors",{{"Data.Column27", each Number.Round(_, 2), type number}, {"Tồn trong kho", each Number.Round(_, 2), type number}, {"Tồn đi đường1", each Number.Round(_, 2), type number}, {"Tồn đi đường", each Number.Round(_, 2), type number}}),
    #"Filtered Rows2" = Table.SelectRows(#"Rounded Off", each ([Data.Column27] <> 0)),
    #"Removed Columns3" = Table.RemoveColumns(#"Filtered Rows2",{"Data.Column27", "Tồn đi đường1"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns3",{{"Tháng", "Thang"}})
in
    #"Renamed Columns1";

shared LastBM8 = let
    data = Excel.CurrentWorkbook(){[Name="Table4"]}[Content],
    forwpath = data{0}[Column1],
    FilePath = forwpath & "Thủy\KHO NĂM 2026\Quyết toán\Biểu 08 TMB-print.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    GOP_Sheet = Source{[Item="GOP",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(GOP_Sheet, [PromoteAllScalars=true]),
    #"Added Custom" = Table.AddColumn(#"Promoted Headers", "Custom", each try Number.From([Tổng cộng tồn kho cuối kỳ]) otherwise 0),
    #"Filtered Rows" = Table.SelectRows(#"Added Custom", each [Custom] > 0.001),
    #"Removed Columns1" = Table.RemoveColumns(#"Filtered Rows",{"Custom"}),
    #"Removed Columns" = Table.RemoveColumns(#"Removed Columns1",{"Tổng cộng tồn kho đầu năm", "Column3", "Trong kho", "Column5", "Đi đường", "Column7", "Gửi bán", "Column9", "Nhập mua", "Column11", "Nhập nội bộ MB", "Column13", "Nhập chế biến", "Column15", "Nhập pha trộn", "Column17", "Nhập nội bộ công ty", "Column19", "Nhập lại hàng ĐĐ", "Column21", "Nhập chuyển đổi", "Column23", "Nhập HH, #(lf)thừa kiểm kê", "Column25", "CL do quy ẩm", "Column27", "Tổng nhập", "Column29", "Xuất bán", "Column31", "Xuất hàng ĐĐ nhập kho", "Column33", "Xuất chế biến", "Column35", "Xuất Pha trộn", "Column37", "Xuất nội bộ Cty", "Column39", "Xuất chuyển đổi", "Column41", "Xuất HH + Thiếu theo K.Kê", "Column43", "Xuất khác", "Column45", "Tổng xuất", "Column47", "Tổng cộng tồn kho cuối kỳ", "Column49", "Đi đường_1", "Column53", "Column58", "Column59", "Column60", "Column61", "Column62", "Column63", "Column64"}),
    #"Renamed Columns1" = Table.RenameColumns(#"Removed Columns",{{"Column56", "Column63"}, {"Column57", "Column64"}}),
    #"Rounded Off" = Table.TransformColumns(#"Renamed Columns1",{{"Tồn trong kho ", each Number.Round(_, 2), type number}}),
    #"Filtered Rows1" = Table.SelectRows(#"Rounded Off", each ([#"Tồn trong kho "] <> 0)),
    #"Rounded Off1" = Table.TransformColumns(#"Filtered Rows1",{{"Column51", each Number.Round(_, 0), type number}}),
    #"Renamed Columns" = Table.RenameColumns(#"Rounded Off1",{{"Chủng loại", "Column1"}, {"Tồn trong kho ", "Column2"}, {"Column51", "Column3"}, {"Column55", "Column4"}, {"Column54", "Column5"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"Column2", type number}, {"Column3", type number}, {"Column5", type number}, {"Column4", type number}}),
    #"Rounded Off2" = Table.TransformColumns(#"Changed Type",{{"Column2", each Number.Round(_, 2), type number}, {"Column3", each Number.Round(_, 2), type number}, {"Column5", each Number.Round(_, 2), type number}, {"Column4", each Number.Round(_, 2), type number}})
in
    #"Rounded Off2";

shared LastBM7 = let
    data = Excel.CurrentWorkbook(){[Name="Table4"]}[Content],
    forwpath = data{0}[Column1],
    FilePath = forwpath & "Thủy\KHO NĂM 2026\Quyết toán\Bao cáo NXT Biểu 07-TMB-print.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    Query1_Sheet = Source{[Item="Query1",Kind="Sheet"]}[Data],
    #"Removed Top Rows" = Table.Skip(Query1_Sheet,4),
    #"Promoted Headers" = Table.PromoteHeaders(#"Removed Top Rows", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Content.Column1", Int64.Type}, {"Content.Column2", type text}, {"Content.Column3", type number}, {"Content.Column4", Int64.Type}, {"Content.Column5", type number}, {"Content.Column6", Int64.Type}, {"Content.Column7", type number}, {"Content.Column8", Int64.Type}, {"Content.Column9", Int64.Type}, {"Content.Column10", Int64.Type}, {"Content.Column11", type number}, {"Content.Column12", Int64.Type}, {"Content.Column13", Int64.Type}, {"Content.Column14", Int64.Type}, {"Content.Column15", Int64.Type}, {"Content.Column16", Int64.Type}, {"Content.Column17", Int64.Type}, {"Content.Column18", Int64.Type}, {"Content.Column19", Int64.Type}, {"Content.Column20", type number}, {"Content.Column21", Int64.Type}, {"Content.Column22", Int64.Type}, {"Content.Column23", Int64.Type}, {"Content.Column24", Int64.Type}, {"Content.Column25", Int64.Type}, {"Content.Column26", type number}, {"Content.Column27", Int64.Type}, {"Content.Column28", Int64.Type}, {"Content.Column29", type number}, {"Content.Column30", type number}, {"Content.Column31", Int64.Type}, {"Content.Column32", Int64.Type}, {"Content.Column33", Int64.Type}, {"Content.Column34", Int64.Type}, {"Content.Column35", Int64.Type}, {"Content.Column36", type number}, {"Content.Column37", Int64.Type}, {"Content.Column38", type number}, {"Content.Column39", Int64.Type}, {"Content.Column40", Int64.Type}, {"Content.Column41", Int64.Type}, {"Content.Column42", Int64.Type}, {"Content.Column43", Int64.Type}, {"Content.Column44", Int64.Type}, {"Content.Column45", Int64.Type}, {"Content.Column46", type number}, {"Content.Column47", Int64.Type}, {"Content.Column48", type number}, {"Content.Column49", Int64.Type}, {"Content.Column50", type number}, {"Content.Column51", Int64.Type}, {"Content.Column52", type number}, {"Content.Column53", Int64.Type}, {"Content.Column54", Int64.Type}, {"Content.Column55", Int64.Type}, {"Content.Column56", Int64.Type}, {"Content.Column57", Int64.Type}, {"Content.Column58", type number}, {"Content.Column59", Int64.Type}, {"Content.Column60", type number}, {"Content.Column61", Int64.Type}, {"Content.Column62", type number}, {"Content.Column63", Int64.Type}, {"Content.Column64", type number}, {"Content.Column65", Int64.Type}, {"Content.Column66", Int64.Type}, {"Content.Column67", Int64.Type}, {"Content.Column68", Int64.Type}, {"Content.Column69", Int64.Type}, {"Content.Column70", type number}, {"Content.Column71", Int64.Type}, {"Content.Column72", type number}, {"Content.Column73", Int64.Type}, {"Content.Column74", type number}, {"Content.Column75", Int64.Type}, {"Content.Column76", type number}, {"Content.Column77", Int64.Type}, {"Content.Column78", Int64.Type}, {"Content.Column79", Int64.Type}, {"Tháng", Int64.Type}}),
    #"Added Custom" = Table.AddColumn(#"Changed Type", "Custom", each try Number.From([Content.Column72]) otherwise 0),
    #"Filtered Rows" = Table.SelectRows(#"Added Custom", each [Custom] > 0.001),
    #"Removed Columns1" = Table.RemoveColumns(#"Filtered Rows",{"Custom"}),
    #"Removed Columns" = Table.RemoveColumns(#"Removed Columns1",{"Content.Column1", "Content.Column3", "Content.Column4", "Content.Column5", "Content.Column6", "Content.Column7", "Content.Column8", "Content.Column9", "Content.Column10", "Content.Column11", "Content.Column12", "Content.Column13", "Content.Column14", "Content.Column15", "Content.Column16", "Content.Column17", "Content.Column18", "Content.Column19", "Content.Column20", "Content.Column21", "Content.Column22", "Content.Column23", "Content.Column24", "Content.Column25", "Content.Column26", "Content.Column27", "Content.Column28", "Content.Column29", "Content.Column30", "Content.Column31", "Content.Column32", "Content.Column33", "Content.Column34", "Content.Column35", "Content.Column36", "Content.Column37", "Content.Column38", "Content.Column39", "Content.Column40", "Content.Column41", "Content.Column42", "Content.Column43", "Content.Column44", "Content.Column45", "Content.Column46", "Content.Column47", "Content.Column48", "Content.Column49", "Content.Column50", "Content.Column51", "Content.Column52", "Content.Column53", "Content.Column54", "Content.Column55", "Content.Column56", "Content.Column57", "Content.Column58", "Content.Column59", "Content.Column60", "Content.Column61", "Content.Column62", "Content.Column63", "Content.Column64", "Content.Column65", "Content.Column66", "Content.Column67", "Content.Column68", "Content.Column69", "Content.Column70", "Content.Column71", "Content.Column72", "Content.Column73"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Columns",{{"Content.Column74", "LuongT"}, {"Content.Column75", "TienT"}, {"Content.Column76", "LuongDD"}, {"Content.Column77", "TienDD"}, {"Content.Column78", "LuongTG"}, {"Content.Column79", "TienTG"}}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Renamed Columns",{{"LuongT", type number}, {"TienT", type number}, {"LuongDD", type number}, {"TienDD", type number}, {"LuongTG", type number}, {"TienTG", type number}}),
    #"Rounded Off" = Table.TransformColumns(#"Changed Type1",{{"LuongT", each Number.Round(_, 2), type number}, {"TienT", each Number.Round(_, 2), type number}, {"LuongDD", each Number.Round(_, 2), type number}, {"TienDD", each Number.Round(_, 2), type number}, {"LuongTG", each Number.Round(_, 2), type number}, {"TienTG", each Number.Round(_, 2), type number}}),
    #"Changed Type2" = Table.TransformColumnTypes(#"Rounded Off",{{"LuongT", type number}, {"TienT", type number}, {"LuongDD", type number}, {"TienDD", type number}})
in
    #"Changed Type2";

shared Mua = let
    data = Excel.CurrentWorkbook(){[Name="Table4"]}[Content],
    forwpath = data{0}[Column1],
    topath = forwpath & "Thủy\Path.xlsx",
    datapath = Excel.Workbook(File.Contents(topath), null, true),
    allpath = datapath{[Item="_2025",Kind="Table"]}[Data],
    backpath = allpath{6}[path],
    FilePath = forwpath & "Thủy\KHO NĂM 2026\HÀNG NHẬP\Hàng nhập 2026.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Name] = "T1" or [Name] = "T10" or [Name] = "T11" or [Name] = "T12" or [Name] = "T2" or [Name] = "T3" or [Name] = "T4" or [Name] = "T5" or [Name] = "T6" or [Name] = "T7" or [Name] = "T8" or [Name] = "T9")),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Item", "Kind", "Hidden"}),
    #"Expanded Data" = Table.ExpandTableColumn(#"Removed Columns", "Data", {"Column1", "Column2", "Column3", "Column4", "Column5", "Column6", "Column7", "Column8", "Column9", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15", "Column16", "Column17", "Column18", "Column19", "Column20", "Column21", "Column22", "Column23", "Column24", "Column25", "Column26", "Column27", "Column28", "Column29", "Column30", "Column31", "Column32", "Column33"}, {"Data.Column1", "Data.Column2", "Data.Column3", "Data.Column4", "Data.Column5", "Data.Column6", "Data.Column7", "Data.Column8", "Data.Column9", "Data.Column10", "Data.Column11", "Data.Column12", "Data.Column13", "Data.Column14", "Data.Column15", "Data.Column16", "Data.Column17", "Data.Column18", "Data.Column19", "Data.Column20", "Data.Column21", "Data.Column22", "Data.Column23", "Data.Column24", "Data.Column25", "Data.Column26", "Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30", "Data.Column31", "Data.Column32", "Data.Column33"}),
    #"Filtered Rows1" = Table.SelectRows(#"Expanded Data", each ([Data.Column2] <> null)),
    #"Promoted Headers" = Table.PromoteHeaders(#"Filtered Rows1", [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"T1", type text}, {"Trạm", type text}, {"Biểu 8", type text}, {"Biểu 7", type text}, {"Kho", type text}, {"NXT", type text}, {"Số HĐ", Int64.Type}, {"Ngày", type date}, {"Số PNK", Int64.Type}, {"CL", type text}, {"pt", type text}, {"Lg chưa QA", type number}, {"Lượng HĐ", type number}, {"Lượng CN chưa QA", type number}, {"Lượng NK", type number}, {"HH", type number}, {"HHQA", type number}, {"Tiền than", Int64.Type}, {"T CP", Int64.Type}, {"VC", Int64.Type}, {"BH", Int64.Type}, {"KC", Int64.Type}, {"VCBX", Int64.Type}, {"Vun gon", Int64.Type}, {"AK", type number}, {"V", type number}, {"W", type number}, {"Q", Int64.Type}, {"S", type number}, {"0", Int64.Type}, {"TD/PT", type text}, {"Lượng đầu nguồn QA", type number}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"T1", "Tháng"}}),
    #"Removed Columns1" = Table.RemoveColumns(#"Renamed Columns",{"NXT", "Số HĐ", "Ngày", "Số PNK", "CL", "AK", "V", "W", "Q", "S"}),
    #"Replaced Value" = Table.ReplaceValue(#"Removed Columns1","T","",Replacer.ReplaceText,{"Tháng"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Replaced Value",{{"Tháng", Int64.Type}}),
    #"Filtered Rows2" = Table.SelectRows(#"Changed Type1", each ([Biểu 8] <> ""))
in
    #"Filtered Rows2";

shared DD = let
    data = Excel.CurrentWorkbook(){[Name="Table4"]}[Content],
    forwpath = data{0}[Column1],
    FilePath = forwpath & "Thủy\KHO NĂM 2026\HÀNG NHẬP\Hàng nhập 2026.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Name] = "T0 (DD)" or [Name] = "T1 (DD)" or [Name] = "T10 (DD)" or [Name] = "T11 (DD)" or [Name] = "T12 (DD)" or [Name] = "T2 (DD)" or [Name] = "T3 (DD)" or [Name] = "T4 (DD)" or [Name] = "T5 (DD)" or [Name] = "T6 (DD)" or [Name] = "T7 (DD)" or [Name] = "T8 (DD)" or [Name] = "T9 (DD)")),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Item", "Kind", "Hidden"}),
    #"Expanded Data" = Table.ExpandTableColumn(#"Removed Columns", "Data", {"Column1", "Column2", "Column3", "Column4", "Column5", "Column6", "Column7", "Column8", "Column9", "Column10", "Column11", "Column12", "Column13", "Column14", "Column15", "Column16", "Column17", "Column18", "Column19", "Column20", "Column21", "Column22", "Column23", "Column24", "Column25", "Column26", "Column27", "Column28", "Column29", "Column30", "Column31", "Column32", "Column33", "Column34", "Column35"}, {"Data.Column1", "Data.Column2", "Data.Column3", "Data.Column4", "Data.Column5", "Data.Column6", "Data.Column7", "Data.Column8", "Data.Column9", "Data.Column10", "Data.Column11", "Data.Column12", "Data.Column13", "Data.Column14", "Data.Column15", "Data.Column16", "Data.Column17", "Data.Column18", "Data.Column19", "Data.Column20", "Data.Column21", "Data.Column22", "Data.Column23", "Data.Column24", "Data.Column25", "Data.Column26", "Data.Column27", "Data.Column28", "Data.Column29", "Data.Column30", "Data.Column31", "Data.Column32", "Data.Column33", "Data.Column34", "Data.Column35"}),
    #"Filtered Rows1" = Table.SelectRows(#"Expanded Data", each ([Data.Column3] <> null)),
    #"Promoted Headers" = Table.PromoteHeaders(#"Filtered Rows1", [PromoteAllScalars=true]),
    #"Renamed Columns1" = Table.RenameColumns(#"Promoted Headers",{{"Column34", "TD"}}),
    #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns1",{{"T0 (DD)", type text}, {"Trạm", type text}, {"Biểu 8", type text}, {"Biểu 7", type text}, {"Kho", type text}, {"NXT", type text}, {"Số HĐ", Int64.Type}, {"Ngày", type date}, {"Số PNK", Int64.Type}, {"CL", type text}, {"pt", type text}, {"Lg chưa QA", type number}, {"Lượng HĐ", type number}, {"Lượng CN chưa QA", type number}, {"Lượng NK", type number}, {"HH", type number}, {"HHQA", type number}, {"Tiền than", Int64.Type}, {"T CP", Int64.Type}, {"VC", Int64.Type}, {"BH", Int64.Type}, {"KC", Int64.Type}, {"VCBX", Int64.Type}, {"Vun gon", Int64.Type}, {"AK", type number}, {"V", type number}, {"W", type number}, {"Q", Int64.Type}, {"S", type number}, {"0", Int64.Type}, {"Column32", type any}, {"TD/PT", type text}, {"TD", type any}}),
    #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"T0 (DD)", "Tháng"}}),
    #"Removed Columns1" = Table.RemoveColumns(#"Renamed Columns",{"NXT", "Số HĐ", "Ngày", "Số PNK", "CL", "AK", "V", "W", "Q", "S"}),
    #"Replaced Value" = Table.ReplaceValue(#"Removed Columns1","T","",Replacer.ReplaceText,{"Tháng"}),
    #"Replaced Value1" = Table.ReplaceValue(#"Replaced Value"," (DD)","",Replacer.ReplaceText,{"Tháng"}),
    #"Replaced Value2" = Table.ReplaceValue(#"Replaced Value1","-12","0",Replacer.ReplaceText,{"Tháng"}),
    #"Changed Type1" = Table.TransformColumnTypes(#"Replaced Value2",{{"Tháng", Int64.Type}}),
    #"Filtered Rows2" = Table.SelectRows(#"Changed Type1", each ([Biểu 8] <> "" and [Biểu 8] <> "0" and [Biểu 8] <> "Biểu 8"))
in
    #"Filtered Rows2";

shared #"Tên cám (2)" = let
    data = Excel.CurrentWorkbook(){[Name="Table4"]}[Content],
    forwpath = data{0}[Column1],
    topath = forwpath & "Thủy\Path.xlsx",
    datapath = Excel.Workbook(File.Contents(topath), null, true),
    allpath = datapath{[Item="_2025",Kind="Table"]}[Data],
    backpath = allpath{0}[path],
    FilePath = forwpath & "Thủy\KHO NĂM 2026\Tổng hợp NXT các trạm 2026.xlsx",
    Source = Excel.Workbook(File.Contents(FilePath), null, true),
    #"Tên cám_Sheet" = Source{[Item="Tên cám",Kind="Sheet"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(#"Tên cám_Sheet",{{"Column1", type text}, {"Column2", type text}, {"Column3", type text}, {"Column4", type text}, {"Column5", type text}}),
    #"Promoted Headers" = Table.PromoteHeaders(#"Changed Type", [PromoteAllScalars=true]),
    #"Changed Type1" = Table.TransformColumnTypes(#"Promoted Headers",{{"Than tại NXT", type text}, {"Biểu 8", type text}, {"Biểu 7", type text}, {"TD", type text}, {"Tên TD", type text}})
in
    #"Changed Type1";