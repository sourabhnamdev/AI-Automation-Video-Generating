package com.videoapp.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.videoapp.service.FfmpegService;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@RestController
@RequestMapping("/video")
public class FFmpegController {

//    @Value("${images.folder.path}")
    String imagesFolderPath="G:\\Automation_Video_Project\\videoapp\\Data\\Images\\Hero Heroin";

//    @Value("${audio.folder.path}")
    String audioFolderPath="G:\\Automation_Video_Project\\videoapp\\Data\\audio";

//    @Value("${slideshow.output.folder.path}")
    String slideshowOutputFolderPath="G:\\Automation_Video_Project\\videoapp\\edit video stores";
    
    @Autowired
    private FfmpegService ffmpegService;

    @PostMapping("/createSlideshow")
    public String createSlideshow(@RequestParam int NumberOfimages) throws InterruptedException {
        try {
            // Step 1: Select 5 random images from 'images' folder
            List<String> selectedImages = selectRandomImagePaths(NumberOfimages);

            // Step 2: Select an audio file from 'audio' folder
            String selectedAudio = selectRandomAudioPath();

            ffmpegService.createSlideshow(selectedImages, selectedAudio, slideshowOutputFolderPath);
 
            return "Slideshow created successfully!";
        } catch (IOException e) {
            e.printStackTrace();
            return "Error creating slideshow!";
        }
    }

    private List<String> selectRandomImagePaths(int count) throws IOException {
        List<File> images = Files.list(Paths.get(imagesFolderPath)).map(Path::toFile).toList();
        List<String> selectedImagePaths = new ArrayList<>();
        Random random = new Random();
        for (int i = 0; i < count; i++) {
            selectedImagePaths.add(images.get(random.nextInt(images.size())).getAbsolutePath());
        }
        return selectedImagePaths;
    }

    private String selectRandomAudioPath() throws IOException {
        List<File> audioFiles = Files.list(Paths.get(audioFolderPath)).map(Path::toFile).toList();
        Random random = new Random();
        return audioFiles.get(random.nextInt(audioFiles.size())).getAbsolutePath();
    }


    private void saveSlideshowToOutputFolder() {
        // Logic to move or copy the created slideshow to the 'outputofslideshow' folder
    }
}
