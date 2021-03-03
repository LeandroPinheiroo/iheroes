package com.gmail.heroes.heroes.web;


import com.gmail.heroes.heroes.builder.UserBuilder;
import com.gmail.heroes.heroes.domain.User;
import com.gmail.heroes.heroes.repository.UserRepository;
import com.gmail.heroes.heroes.security.RunWithMockCustomUser;
import com.gmail.heroes.heroes.util.TestUtil;
import com.gmail.heroes.heroes.web.dto.UserDTO;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureMockMvc
public class UserResourceIt {

    private static final String API = "/api/user";

    @MockBean
    private UserRepository userRepository;

    @Autowired
    private MockMvc mockMvc;

    private UserBuilder userBuilder = new UserBuilder();

    @Test
    @RunWithMockCustomUser
    public void saveUser() throws Exception {
        UserDTO userDTO = userBuilder.mountUserDto();
        User user = new User();
        user.setName(userDTO.getName());
        user.setEmail(userDTO.getEmail());
        when(userRepository.save(any())).thenReturn(user);
        mockMvc.perform(post(API)
                .contentType(TestUtil.APPLICATION_JSON_UTF8)
                .content(TestUtil.convertObjectToJsonBytes(userDTO))
                .contentType(TestUtil.APPLICATION_JSON_UTF8))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value(user.getName()));

    }
}