import cv2 as cv

img_input = input("Enter filename: ")
img = cv.imread(img_input, cv.IMREAD_UNCHANGED)

print('Dimensions: ', img.shape)
resize_width = int(input("New width: "))
resize_height = int(input("New height: "))

dimensions = (resize_width, resize_height)

img_output = cv.resize(img, dimensions, interpolation= cv.INTER_AREA)

cv.imshow("Resized image", img_output)
cv.imwrite(img_input, img_output)
cv.waitKey(0)
cv.destroyAllWindows()