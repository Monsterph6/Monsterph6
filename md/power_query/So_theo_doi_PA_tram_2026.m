section Section1;

shared Tồn = let
    Source = Excel.Workbook(Web.Contents("https://thanmb-my.sharepoint.com/personal/nguyenthuthuy_thanmienbac_vn/Documents/Th%E1%BB%A7y/KHO%20N%C4%82M.2023/QTKVCP%202023/QT%20PTNK%20H%E1%BA%A3i%20Ph%C3%B2ng%202023.xlsx"), null, true),
    Tồn_Sheet = Source{[Item="Tồn",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Tồn_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Trạm", type text}, {"Than thu hồi", type text}, {"Than Đưa vào PT", type text}, {"AK", type number}, {"Vk", type number}, {"Qk", Int64.Type}, {"Sk", type number}, {"KL đưa vào PT", type number}, {"KL nghiệm thu", type number}, {"Đơn giá", Int64.Type}, {"Lượng tồn", type number}})
in
    #"Changed Type";