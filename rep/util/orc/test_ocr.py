import easyocr

reader = easyocr.Reader(['ch_sim', 'en'])

order_images = ["order.jpg", "order_2.jpg", "order_3.jpg", "order_4.jpg"]

for image in order_images:
    result = reader.readtext(image, detail=0)
    for i in range(0, len(result)):
        order_id = ""
        if result[i] == "商家订单号" or result[i] == "商户单号":
            order_id = result[i + 1]
        if "订单编号: " in result[i]:
            order_id = result[i].replace("订单编号: ", "")

        if order_id == "":
            continue

        if "0P" in order_id:
            order_id = order_id.replace("0P", "OP")
        if " " in order_id:
            order_id = order_id.replace(" ", "")

        print(image, order_id)

print(reader.readtext("order_1.jpg", detail=0))