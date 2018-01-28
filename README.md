# ilet


To analyze video files, run ```ensemble.py```, making sure to change ```video_filename``` and ```audio_filename```. The file will split the video into natural segments as well as classify each one as a clap, music, or speech.

You may need to change ```low,high``` (the number of segments to split the video into) to get the proper classification analysis. Hopefully, we will think of a way to code this in!

To analyze video snippets, we processed screenshots of the split files with PyTorch. The image captioning tutorial is made by [@yunjey](https://github.com/yunjey/pytorch-tutorial/tree/master/tutorials/03-advanced/image_captioning). Following the instructions detailed in the Usage, we can then test the model by calling:
```
$ python sample.py --image='png/example.png'
```
