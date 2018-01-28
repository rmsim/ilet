

To analyze video snippets, we processed screenshots of the split files with PyTorch. The image captioning tutorial is made by [@yunjey](https://github.com/yunjey/pytorch-tutorial/tree/master/tutorials/03-advanced/image_captioning). Following the instructions detailed in the Usage, we can then test the model by calling:
```
$ python sample.py --image='png/example.png'

```


Instructions for Video analysis:

1. Make video with PhotoBooth Save video and place in image captioning folder.

2. Analyze the video audio! Split your video in pieces based off of sound cues. 

Run
```
python ensemble.py "test.mov" "test.wav" "test_registry.txt"
```
Where the arguments are the name of the video you just made, a name for the corresponding audio file, and a name for a registry that maps video segment file to sound classification.

You may need to change ```low,high``` (the number of segments to split the video into) to get the proper classification analysis. Hopefully, we will think of a way to code this in!

3. Analyze the video pictures! Classify what's in each video segment and store it for the iLet app to use later.

Run
```
python sample.py --textfile "test_registry.txt" "test_tags.txt"
```
Where the arguments are the registry file from above and a name for the image classifications within each video segment.

# iLet for SheHacks'18







