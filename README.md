# Image-Steganography

### Interface....

![Main Interface](https://user-images.githubusercontent.com/68480967/89532737-e4071580-d80f-11ea-94b8-4b5d3d7869e0.jpg)

![Interface](https://user-images.githubusercontent.com/68480967/89532340-46abe180-d80f-11ea-939f-5e4342d632a1.jpg)

##### >> Image steganography refers to hiding information i.e. text, images or audio files in another image or video files. The current project aims to use steganography for an text with another image using LSB.
>
>> Here we embedd each character ( ascii value which is converted into binary 8-bit form) into 3 pixels of an image.
>
>> 8 of the 9 pixels are used to store the character information and the last pixel is used to check weather this is last character of input text.
>
>> let [r1, g1, b1], [r2, g2, b2], [r3 ,g3, b3] be the three pixels in which we have to store a character.
>> let "a" be the character => ascii value = 65 => binary of 65 = 01000001
>> Now assigning r1 to g3 for all 8-bits.
>> Check if r1%2 == d7 (MSB), and for other pixels...
>> If it is not true, then change the pixel value by 1 ( add or subtract )
>> (0, 1, 0, 0, 0, 0, 0, 1) = (r1%2, g1%2, b1%2, r2%2, g2%2, b2%2, r3%2, g3%2)
>> Once we have this check b3, if this is our last character then b3%2 must be 0 else 1
>> For extraction, we simply take 3 pixels at a time and using "%" operation on first 8 pixels we get the character
>> Continue this process untill we get b3%2 == 0
>
>> For security purposes, we encrypt the actual text using key and my encryption algorithm.
>> So if we use the wromng key we will get garbage values.
>
>> If we save our text-embedded image into '.jpg' format then the information will be lost due to lossy compression of JPEG.
>> Hence saving our text into '.png' format which has lossless compression.
