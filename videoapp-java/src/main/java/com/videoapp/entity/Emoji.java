package com.videoapp.entity;

import java.time.LocalDate;

import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Data
@Table(name = "emojis")
public class Emoji {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	private String name;
	private String category;
	@Lob
	@Column(columnDefinition = "BLOB")
	private byte[] emoji; // Store emoji image as byte array

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
