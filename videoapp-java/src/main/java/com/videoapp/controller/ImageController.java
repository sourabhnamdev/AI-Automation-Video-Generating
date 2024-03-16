package com.videoapp.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.videoapp.entity.Image;
import com.videoapp.loader.PinterestScraperService;

@RestController
@RequestMapping("/images")
public class ImageController {

	@Autowired
	private PinterestScraperService scraperService;

	@GetMapping("/scrape-images")
	public List<Image> scrapeImages(@RequestParam String boardUrl, @RequestParam String category) {
		List<Image> images = null;
		if (!category.isEmpty()) {
			images = scraperService.scrapeImagesFromBoard(boardUrl,category);
		}

		return images;
	}

}