package com.videoapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

@SpringBootApplication
@EnableJpaAuditing
public class VideoappApplication {

	public static void main(String[] args) {
		SpringApplication.run(VideoappApplication.class, args);
	}

}
