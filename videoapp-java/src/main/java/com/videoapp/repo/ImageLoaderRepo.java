package com.videoapp.repo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.videoapp.entity.Image;

@Repository
public interface ImageLoaderRepo extends JpaRepository<Image, Long> {

}
