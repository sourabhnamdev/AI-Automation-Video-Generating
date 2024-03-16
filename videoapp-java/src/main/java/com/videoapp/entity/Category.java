package com.videoapp.entity;

import java.time.LocalDate;

import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "categories")
public class Category{
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	private String categoryName;
	
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
