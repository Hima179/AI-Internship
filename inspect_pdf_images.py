import pymupdf

doc = pymupdf.open(r"D:\AI INTERNSHIP\SandeshHalmadge_SIP_WeeklyReport.pdf")
for i, page in enumerate(doc):
    imgs = page.get_images()
    print(f"Page {i+1} images: {len(imgs)}")
    for j, img in enumerate(imgs):
        xref = img[0]
        base_img = doc.extract_image(xref)
        print(f"  Img {j}: xref={xref}, ext={base_img['ext']}, bytes={len(base_img['image'])}, dim={base_img['width']}x{base_img['height']}")
        if i == 0 and j == 0:
            with open(r"d:\AI INTERNSHIP\sandesh_extracted_logo.png", "wb") as f:
                f.write(base_img['image'])

print("Done inspecting PDF images.")
