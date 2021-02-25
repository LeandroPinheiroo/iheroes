package com.gmail.heroes.heroes.web.dto;


import lombok.Getter;
import lombok.Setter;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

@Getter
@Setter
public class UserDTO {

    private Long id;

    @NotNull(message = "Nome obrigatório")
    @NotBlank(message = "Nome obrigatório")
    private String name;

    @NotNull(message = "E-mail é obrigatório")
    @NotBlank(message = "E-mail é obrigatório")
    @Email(message = "E-mail inválido")
    private String email;

    @NotNull(message = "Senha é obrigatório")
    @NotBlank(message = "Senha é obrigatório")
    private String password;

}
