package com.gmail.heroes.heroes.web;


import com.gmail.heroes.heroes.service.UserService;
import com.gmail.heroes.heroes.web.dto.UserDTO;
import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;


@RestController
@RequestMapping("/api/user")
@RequiredArgsConstructor
@Validated
public class UserResource {

    private final UserService userService;
    private final Logger log = LoggerFactory.getLogger(UserResource.class);

    /**
     * POST /api/user: request to save a user
     *
     * @return UserDto object saved
     */
    @PostMapping
    public ResponseEntity<UserDTO> save(@Valid @RequestBody UserDTO userDTO) {
        log.debug("Request to save a new user, {}",userDTO);
        return ResponseEntity.ok(userService.save(userDTO));
    }

}
