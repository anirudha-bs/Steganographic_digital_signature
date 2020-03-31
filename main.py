import stegno
import cv2

print("----- Stegnographic digital signature -----")
print("1.Digitally sign the image")
print("2.Verify the authenticity of the image")
option = int(input("Enter your option - "))

if option == 1:
    signed_image = stegno.encode()
    name = 'Signed_image.png'
    cv2.imwrite(name, signed_image)
    print("Signed image saved as (Signed_image.png)")

elif option == 2:
    result = stegno.decode()
    if result:
        print("Digital signature verified")
    else:
        print("Digital signature is invalid")

else:
    raise Exception("Enter correct input")
