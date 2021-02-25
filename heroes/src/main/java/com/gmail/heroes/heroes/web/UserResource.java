package com.gmail.heroes.heroes.web;


import com.gmail.heroes.heroes.service.UserService;
import com.gmail.heroes.heroes.web.dto.UserDTO;
import lombok.RequiredArgsConstructor;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.annotation.Secured;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.slf4j.Logger;

import javax.validation.Valid;
import java.util.List;


@RestController
@RequestMapping("/api/user")
@RequiredArgsConstructor
@Validated
public class UserResource {

    private final UserService userService;
    private final Logger log = LoggerFactory.getLogger(UserResource.class);


    /**
     * Get /api/user: request to save a user
     *
     * @return UserDto object saved
     */
    @GetMapping
    public ResponseEntity<List<UserDTO>> findAll() {
        log.debug("Request to get all users");
        return ResponseEntity.ok(userService.findAll());
    }

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
