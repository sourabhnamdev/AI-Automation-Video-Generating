package com.videoapp.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;

import java.io.*;
import java.net.MalformedURLException;
import java.nio.file.*;
import java.util.Date;
import java.util.Map;

@CrossOrigin
@Controller
@RequestMapping("/api/videos")
public class VideoController {
	
	final String ffmpeg="C:\\FFmpeg\\bin\\ffmpeg";

	private final Path videoLocation = Paths.get("G:\\Automation_Video_Project\\videoapp\\videos stores");
	private final Path editVideoLocation = Paths.get("G:\\Automation_Video_Project\\videoapp\\edit video stores");
	
	@GetMapping("/videoappweb.html")
	public String videoAppWeb() {
		return "forward:/videoappweb.html";
	}

	@GetMapping("/videoappstyle.css")
	public String videoAppStyle() {
		return "forward:/videoappstyle.css";
	}

	@GetMapping("/videoappaction.js")
	public String videoAppAction() {
		return "forward:/videoappaction.js";
	}

	@PostMapping("/upload")
	public ResponseEntity<?> uploadVideo(@RequestParam("video") MultipartFile file) {
		try {
			if (file.isEmpty()) {
				return ResponseEntity.badRequest().body("No video file provided");
			}
			// Save the file on the server
			String fileName = file.getOriginalFilename();
			Path targetLocation = this.videoLocation.resolve(fileName);
			Files.copy(file.getInputStream(), targetLocation, StandardCopyOption.REPLACE_EXISTING);
			System.out.print("Video uploaded successfully: " + fileName);
			return ResponseEntity.ok().body(fileName);
		} catch (IOException ex) {
			return ResponseEntity.internalServerError().body("Could not store video file: " + ex.getMessage());
		}
	}

	@PostMapping("/cut")
	public ResponseEntity<?> cutVideo(@RequestBody Map<String, String> payload) {
		try {
			String fileName = payload.get("fileName");
			String startTime = payload.get("startTime");
			String endTime = payload.get("endTime");
			String inputFilePath = videoLocation.resolve(fileName).toString();
			String outputFilePath = editVideoLocation.resolve("cut_" + fileName).toString();
			
			// Validate input parameters
	        if (fileName == null || startTime == null || endTime == null) {
	            return ResponseEntity.badRequest().body("Missing required parameters");
	        }

			// Execute FFmpeg command to cut video
			ProcessBuilder processBuilder = new ProcessBuilder(ffmpeg, "-i", inputFilePath, "-ss", startTime, "-t",
					endTime, "-c", "copy", outputFilePath);
			
			Process process = processBuilder.start();
			process.waitFor();

			return ResponseEntity.ok().body("Video cut successfully");
		} catch (Exception ex) {
			System.out.println(ex.getStackTrace());
			return ResponseEntity.internalServerError().body("Video cut failed: " + ex.getMessage());
		}
	}

	@PostMapping("/trim")
	public ResponseEntity<?> trimVideo(@RequestBody Map<String, String> payload) {
		try {
			String fileName = payload.get("fileName");
			String startTime = payload.get("startTime");
			String endTime = payload.get("endTime");
			String inputFilePath = videoLocation.resolve(fileName).toString();
			String outputFilePath = editVideoLocation.resolve("trim_" + fileName).toString();
			
			// Validate input parameters
	        if (fileName == null || startTime == null || endTime == null) {
	            return ResponseEntity.badRequest().body("Missing required parameters");
	        }

			// Execute FFmpeg command to trim video
			ProcessBuilder processBuilder = new ProcessBuilder(ffmpeg, "-i", inputFilePath, "-vf",
					"trim=start=" + startTime + ":end=" + endTime, "-c", "copy", outputFilePath);
			Process process = processBuilder.start();
			process.waitFor();

			return ResponseEntity.ok().body("Video trim successfully");
		} catch (Exception ex) {
			return ResponseEntity.internalServerError().body("Video trim failed: " + ex.getMessage());
		}
	}

	@GetMapping("/download/{fileName:.+}")
	public ResponseEntity<Resource> downloadVideo(@PathVariable String fileName) {
		try {
			Path filePath = videoLocation.resolve(fileName).normalize();
			Resource resource = new UrlResource(filePath.toUri());
			if (resource.exists()) {
				return ResponseEntity.ok().contentType(MediaType.parseMediaType("application/octet-stream"))
						.header(HttpHeaders.CONTENT_DISPOSITION,
								"attachment; filename=\"" + resource.getFilename() + "\"")
						.body(resource);
			} else {
				return ResponseEntity.notFound().build();
			}
		} catch (MalformedURLException ex) {
			return ResponseEntity.badRequest().body(null);
		}
	}

}
