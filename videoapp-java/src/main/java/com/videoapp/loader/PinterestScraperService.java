package com.videoapp.loader;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import javax.imageio.ImageIO;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.videoapp.entity.Image;
import com.videoapp.repo.ImageLoaderRepo;

@Service
public class PinterestScraperService {

	@Autowired
	private ImageLoaderRepo imageLoaderRepo;

	public List<Image> scrapeImagesFromBoard(String boardUrl, String category) {
	    List<Image> imageList = new ArrayList<>();
	    try {
	        // Fetch the Pinterest board page
	        Document document = Jsoup.connect(boardUrl).get();
	        // Find all anchor elements containing images
	        Elements anchorElements = document.select("a");
	        // Create directory to save images
	        String baseDirectoryPath = "G:\\Automation_Video_Project\\videoapp\\Data\\Images\\";
	        File baseDirectory = new File(baseDirectoryPath);
	        if (!baseDirectory.exists()) {
	            baseDirectory.mkdirs();
	        }
	        // Determine category directory
	        File categoryDirectory = new File(baseDirectory, category);
	        if (!categoryDirectory.exists()) {
	            categoryDirectory.mkdirs();
	        }
	        // Use a ThreadPool for concurrent downloading
	        ExecutorService executor = Executors.newFixedThreadPool(10); // Adjust the thread pool size as needed
	        for (Element anchorElement : anchorElements) {
	            // Check if the anchor contains an image
	            Element imageElement = anchorElement.selectFirst("img[src]");
	            if (imageElement != null) {
	                String imageUrl = imageElement.attr("src");
	                executor.submit(() -> {
	                    try {
	                        // Download image
	                        BufferedImage image;
	                        HttpURLConnection connection = (HttpURLConnection) new URL(imageUrl).openConnection();
	                        connection.setInstanceFollowRedirects(true); // Handle redirects
	                        try (InputStream inputStream = connection.getInputStream()) {
	                            image = ImageIO.read(inputStream);
	                        }
	                        File outputFile = new File(categoryDirectory, "image_" + System.currentTimeMillis() + ".jpg");
	                        ImageIO.write(image, "jpg", outputFile);
	                        // Save image details to database
	                        Image imageEntity = new Image();
	                        imageEntity.setCategory(category);
	                        imageEntity.setImageUrl(imageUrl);
	                        imageEntity.setCreatedDate(LocalDate.now());
	                        imageEntity.setImagePath(outputFile.getAbsolutePath());
	                        imageLoaderRepo.save(imageEntity);
	                        imageList.add(imageEntity);
	                    } catch (IOException e) {
	                        // Log the error
	                        System.out.println(e.getStackTrace());
	                    }
	                });
	            }
	        }
	        executor.shutdown();
	        executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
	        return imageList;
	    } catch (IOException e) {
	        // Rollback the transaction in case of exception
	        imageList.clear();
	        throw new RuntimeException("Failed to scrape images from board: " + boardUrl, e);
	    } catch (InterruptedException e) {
	        Thread.currentThread().interrupt();
	        throw new RuntimeException("Thread interrupted while waiting for image download completion", e);
	    }
	}

}
