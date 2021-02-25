package com.gmail.heroes.heroes.service.mapper;


import com.gmail.heroes.heroes.domain.User;
import com.gmail.heroes.heroes.web.dto.UserDTO;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.Named;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@Mapper(componentModel = "spring")
public interface UserMapper {

    UserDTO toDto(User user);

    List<UserDTO> toDto(List<User> user);


    @Mapping(source = "password", target = "password", qualifiedByName = "getPasswordCrypt")
    User toEntity(UserDTO userDTO);


    @Named("getPasswordCrypt")
    default String getPasswordCrypt(String password) {
        return new BCryptPasswordEncoder().encode(password);
    }


}
