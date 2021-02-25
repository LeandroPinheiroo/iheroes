package com.gmail.heroes.heroes.service;

import com.gmail.heroes.heroes.repository.UserRepository;
import com.gmail.heroes.heroes.service.mapper.UserMapper;
import com.gmail.heroes.heroes.web.dto.UserDTO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;

@Service
@RequiredArgsConstructor
@Transactional
@Slf4j
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;

    public UserDTO save(UserDTO userDTO){
        return this.userMapper.toDto(this.userRepository.save(this.userMapper.toEntity(userDTO)));
    }

}
