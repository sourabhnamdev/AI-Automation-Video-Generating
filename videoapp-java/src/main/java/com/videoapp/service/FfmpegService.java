package com.videoapp.service;

import java.io.IOException;
import java.util.List;

import org.springframework.stereotype.Service;
@Service
public class FfmpegService {
	final String ffmpeg="C:\\FFmpeg\\bin\\ffmpeg ";

	  public void cutVideo(String inputVideo, String outputVideo, int startTime, int duration) {
	        String ffmpegCommand = ffmpeg+"-i " + inputVideo + " -ss " + startTime + " -t " + duration + " -c copy " + outputVideo;
	        executeFfmpegCommand(ffmpegCommand);
	    }
	  public void createSlideshow(List<String> imageFiles, String audioFile, String outputVideo) {
		    StringBuilder imageList = new StringBuilder();
		    for (String imageFile : imageFiles) {
		        imageList.append("-loop 1 -i ").append(imageFile).append(" ");
		    }
		    String ffmpegCommand = ffmpeg + imageList + "-i \"" + audioFile + "\" -vf \"scale=-2:240,format=yuv420p\" -c:v libx264 -b:v 500k -profile:v main -level 3.1 -r 30 -pix_fmt yuv420p \"" + outputVideo + "\"";
		    executeFfmpegCommand(ffmpegCommand);
		}


	    
	    

	    public void applyEffects(String inputVideo, String outputVideo, String effect) {
	        String ffmpegCommand = ffmpeg +" -i " + inputVideo + " -vf " + effect + " -c:a copy " + outputVideo;
	        executeFfmpegCommand(ffmpegCommand);
	    }

	    private void executeFfmpegCommand(String ffmpegCommand) {
	        try {
	         
	        	ProcessBuilder processBuilder = new ProcessBuilder(ffmpegCommand);
	            Process process = processBuilder.start();
			
	       
	            int exitCode = process.waitFor();
	            if (exitCode == 0) {
	                System.out.println("FFmpeg command executed successfully!");
	            } else {
	                System.out.println("Error executing FFmpeg command!");
	            }
	        } catch (IOException | InterruptedException e) {
	            e.printStackTrace();
	        }
	    }
}
