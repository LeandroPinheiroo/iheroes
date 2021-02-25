package com.gmail.heroes.heroes.security;

import com.gmail.heroes.heroes.domain.User;

import java.util.Collections;

public class UserSystem extends org.springframework.security.core.userdetails.User {

	private static final long serialVersionUID = 1L;

	private User user;

	public UserSystem(User user) {
		super(user.getEmail(), user.getPassword(), Collections.emptyList());
		this.user = user;
	}

	public User getUsuario() {
		return user;
	}

}
