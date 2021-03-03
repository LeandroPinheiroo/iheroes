package com.gmail.heroes.heroes.builder;

import com.gmail.heroes.heroes.web.dto.UserDTO;
public class UserBuilder {


    public UserDTO mountUserDto(){
        UserDTO userDTO = new UserDTO();
        userDTO.setPassword("password_test");
        userDTO.setName("Teste Name");
        userDTO.setEmail("test@email.com");
        return userDTO;
    }

}
