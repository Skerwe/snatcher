from pathlib import Path
import re

pages_path = Path('/home/quintin/eaf/environment/development/develop/web/workplaceLivingServices/web/app')
style_path = Path('/home/quintin/eaf/environment/development/develop/web/workplaceLivingServices/web/content/css')
images_path = Path('/home/quintin/eaf/environment/development/develop/web/workplaceLivingServices/web/content/images')

pages = []
styles = []
images = {}
orphan_images = {}

for page in sorted(pages_path.rglob('*')):
    if page.name.endswith(('.html', '.js')):
        pages.append(page)

for style in sorted(style_path.rglob('*')):
    if style.name.endswith(('.css', '.scss')):
        styles.append(style)

for image in sorted(images_path.rglob('*')):
    if image.name.endswith(('.jpg', '.png', '.gif')):
        images[image.name] = [image, False, 0]


def find_orphan_images(files):
    for file in files:
        content = open(file, 'r').read()
        images_references = re.findall(r'[\w-]+.(?:png|jpg)', content, re.I)
        if images_references:
            for image_reference in images_references:
                if image_reference not in images:
                    orphan_images[image_reference] = page.name


def find_referenced_images(files):
    for file in files:
        content = open(file, 'r').read()
        for name in images.keys():
            if name in content:
                images[name][1] = True
                images[name][2] = images[name][2] + 1


find_orphan_images(pages)
find_orphan_images(styles)

find_referenced_images(pages)
find_referenced_images(styles)

# for image in images.items():
#     if image[1][1]:
#         print('%s %s %d' % (image[0], image[1][1], image[1][2]))

count = 0
print('\n\nImages that are not referenced in HTML, JavaScript or in the style files:')
for image in images.items():
    if not image[1][1]:
        print(image[0])
        count += 1

print('\nFound %d orphan images' % count)

print('\n\nImages referenced in HTML, JavaScript or style files that does not exists:')
for image in orphan_images.items():
    print(image)

print('\nFound %d orphan images' % len(orphan_images))
