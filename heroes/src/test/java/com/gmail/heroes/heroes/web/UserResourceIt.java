package com.gmail.heroes.heroes.web;


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

    @Test
    @RunWithMockCustomUser
    public void buscarDemostrativoFilter() throws Exception {
        when(userRepository.save(any())).thenReturn(new User());
        UserDTO userDTO = new UserDTO();
        userDTO.setName("a");
        userDTO.setEmail("testeNOVO123@gmail.com");
        userDTO.setPassword("1234567");
        mockMvc.perform(post(API)
                .contentType(TestUtil.APPLICATION_JSON_UTF8)
                .content(TestUtil.convertObjectToJsonBytes(userDTO))
                .contentType(TestUtil.APPLICATION_JSON_UTF8))
                .andExpect(status().isOk());
    }
}