package com.videoapp.entity;

import java.time.LocalDate;

import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Data;

@Entity
@Data
@Table(name = "videos")
public class Video {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long videoId;

	@ManyToOne
	@JoinColumn(name = "user_id", nullable = false)
	private User user;

	@Column(nullable = false)
	private String originalFilename;

	@Column(nullable = false)
	private String title;

	private String description;
	private String fileUrl;
	private String status;

	@Column(nullable = false)
	private String storagePath;

	@Column(name = "created_by")
	private String createdBy;

	@Column(name = "created_date")
	@CreatedDate // Automatically set by Hibernate
	private LocalDate createdDate;

	@Column(name = "updated_by")
	private String updatedBy;

	@Column(name = "updated_date")
	@LastModifiedDate // Automatically set by Hibernate
	private LocalDate updatedDate;
}
