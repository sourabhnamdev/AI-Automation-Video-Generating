package com.videoapp.repo;

import org.springframework.data.jpa.repository.JpaRepository;

import com.videoapp.entity.Emoji;

public interface EmojiLoaderRepo extends JpaRepository<Emoji, Long> {

}
