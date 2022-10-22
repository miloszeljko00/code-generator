model_template = """package {{project_name}}.model.{{underscore(class.name)}};

import lombok.*;
import javax.persistence.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Entity(name = "{{class.name}}")
@Table(name = "{{underscore(class.name)}}")
public class {{class.name}} {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    {% for property in class.properties -%}
    @Column(name = "{{underscore(property.name)}}")
    private {{ property.type }} {{ property.name }};
        
    {% endfor %}

}"""

dto_template = """package {{project_name}}.dto.{{underscore(class.name)}};

import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class {{class.name}}Dto {
    {% for property in class.properties -%}
    private {{ property.type }} {{ property.name }};
    {% endfor %}
}"""

dtos_template = """package {{project_name}}.dto.{{underscore(class.name)}};

import lombok.*;

import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class {{class.name}}Dtos {
    private List<{{class.name}}Dto> {{class.name.lower()}}s;

    public {{class.name}}Dtos() { this.{{class.name.lower()}}s = new ArrayList<>();}

}"""

repository_interface_template = """package {{project_name}}.repository.{{underscore(class.name)}};

import {{project_name}}.model.{{underscore(class.name)}}.{{class.name}};

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface {{class.name}}Repository extends JpaRepository<{{class.name}}, {{class.properties[0}.type}> {

}"""

service_interface_template = """package {{project_name}}.service.{{underscore(class.name)}};

import {{project_name}}.model.{{underscore(class.name)}}.{{class.name}};

import org.springframework.stereotype.Service;
import java.util.List;

@Service
public interface {{class.name}}Service {
    {{class.name}} create({{class.name}} {{class.name.lower()}});
    List<{{class.name}}> findAll();
    {{class.name}} findBy{{camelize(class.properties[0].name)}}({{class.properties[0].type}} {{class.properties[0].name}});
    {{class.name}} update({{class.name}} {{class.name.lower()}});
    boolean delete({{class.properties[0].type}} {{class.properties[0].name}});
}"""

service_template = """package {{project_name}}.service.{{underscore(class.name)}};

import {{project_name}}.model.{{underscore(class.name)}}.{{class.name}};
import {{project_name}}.repository.{{underscore(class.name)}}.{{class.name}}Repository;

import lombok.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class {{class.name}}ServiceImpl implements {{class.name}}Service {

    private final {{class.name}}Repository {{class.name.lower()}}Repository;

    public {{class.name}} create({{class.name}} {{class.name.lower()}}) {
        if({{class.name.lower()}} == null) return null;
        return {{class.name.lower()}}Repository.save({{class.name.lower()}});
    }

    public List<{{class.name}}> findAll() {
        return {{class.name.lower()}}Repository.findAll();
    }

    public {{class.name}} findBy{{camelize(class.properties[0].name)}}({{class.properties[0].type}} {{class.properties[0].name}}) {
        return {{class.name.lower()}}Repository.findBy{{camelize(class.properties[0].name)}}({{class.properties[0].name}}).orElse(null);
    }

    public {{class.name}} update({{class.name}} {{class.name.lower()}}) {
        if({{class.name.lower()}} == null) return null;
        {{class.name}} old{{class.name}} = {{class.name.lower()}}Repository.findBy{{camelize(class.properties[0].name)}}({{class.name.lower()}}.get{{camelize(class.properties[0].name)}}()).orElse(null);
        if(old{{class.name}} == null) return null;

        return {{class.name.lower()}}Repository.save({{class.name.lower()}});
    }

    public boolean delete({{class.properties[0].type}} {{class.properties[0].name}}) {
        {{class.name}} {{class.name.lower()}} = {{class.name.lower()}}Repository.findBy{{camelize(class.properties[0].name)}}({{class.properties[0].name}}).orElse(null);
        if({{class.name.lower()}} == null) return false;
        {{class.name.lower()}}Repository.delete({{class.name.lower()}});
        return true;
    }
}"""

mapper_interface_template = """package {{project_name}}.mapper.{{underscore(class.name)}};

import {{project_name}}.dto.{{underscore(class.name)}}.{{class.name}}Dto;
import {{project_name}}.model.{{underscore(class.name)}}.{{class.name}};

import org.springframework.stereotype.Service;

@Service
public interface LabelMapper {
    LabelDto toDto(Label label);
    Label toEntity(LabelDto labelDto);
}"""

mapper_template = """package {{project_name}}.mapper.{{underscore(class.name)}};

import {{project_name}}.dto.{{underscore(class.name)}}.{{class.name}}Dto;
import {{project_name}}.model.{{underscore(class.name)}}.{{class.name}};

import org.springframework.stereotype.Service;

@Service
public class {{class.name}}MapperImpl {
    public {{class.name}}Dto toDto({{class.name}} {{class.name.lower()}}) {
        if({{class.name.lower()}} == null) return null;
        return {{class.name}}Dto.builder()
                {% for property in class.properties -%}
                .{{property.name}}({{class.name}}.get{{camelize({{property.name}})}}())
                {% endfor %}
                .build();
    }

    public {{class.name}} toEntity({{class.name}}Dto {{class.name.lower()}}Dto) {
        if({{class.name.lower()}}Dto == null) return null;
        return {{class.name}}.builder()
                {% for property in class.properties -%}
                .{{property.name}}({{class.name}}Dto.get{{camelize({{property.name}})}}())
                {% endfor %}
                .build();
    }
}"""


controller_template = """package {{project_name}}.controller.{{underscore(class.name)}};

import {{project_name}}.dtos.{{underscore(class.name)}}.{{class.name}}Dto;
import {{project_name}}.dtos.{{underscore(class.name)}}.{{class.name}}Dtos;

import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;



@RestController
@RequiredArgsConstructor
@RequestMapping("api/{{underscore(class.name)}}")
public class {{class.name}}Controller {

    private final {{class.name}}Service {{class.name.lower()}}Service;
    private final {{class.name}}Mapper {{class.name.lower()}}Mapper;

    @PostMapping("/create")
    public ResponseEntity<Object> create(@RequestBody {{class.name}}Dto {{class.name.lower()}}Dto) {
        var {{class.name.lower()}} = {{class.name.lower()}}Mapper.toEntity({{class.name.lower()}}Dto);
        var response = {{class.name.lower()}}Service.create({{class.name.lower()}});

        if(response == null) {
            return new ResponseEntity<>("Can't create {{class.name}}, invalid format.", HttpStatus.BAD_REQUEST);
        }
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    @GetMapping
    public ResponseEntity<Object> getAll() {
        var {{class.name.lower()}}s = {{class.name.lower()}}Service.findAll().stream().map({{class.name.lower()}}Mapper::toDto).toList();

        var response = {{class.name}}Dtos.builder()
                                    .{{class.name.lower()}}s({{class.name.lower()}}s)
                                .build();
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    @GetMapping("/{% raw %}{{% endraw %}{{class.properties[0].name}}{% raw %}}{% endraw %}")
    public ResponseEntity<Object> getBy{{camelize(class.properties[0].name)}}(@PathVariable {{class.properties[0].type}} {{class.properties[0].name}}) {
        var {{class.name.lower()}} = {{class.name.lower()}}Service.findBy{{camelize(class.properties[0].name)}}(id);
        var response = {{class.name.lower()}}Mapper.toDto({{class.name.lower()}});

        if(response == null){
            return new ResponseEntity<>("{{class.name}} not found.", HttpStatus.NOT_FOUND);
        }
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    @PutMapping("/{% raw %}{{% endraw %}{{class.properties[0].name}}{% raw %}}{% endraw %}/update")
    public ResponseEntity<Object> update(@PathVariable {{class.properties[0].type}} {{class.properties[0].name}}, @RequestBody {{class.name}}Dto {{class.name.lower()}}Dto) {
        var {{class.name.lower()}} = {{class.name.lower()}}Mapper.toEntity({{class.name.lower()}}Dto);
        if({{class.name.lower()}}.get{{camelize(class.properties[0].name)}}() != {{class.properties[0].name}}) {
            return new ResponseEntity<>("{{class.properties[0].name}} in path and body do not match", HttpStatus.BAD_REQUEST);
        }

        {{class.name.lower()}} = {{class.name.lower()}}Service.update({{class.name.lower()}});

        var response = {{class.name.lower()}}Mapper.toDto({{class.name.lower()}});
        if(response == null) {
            return new ResponseEntity<>("Can't update {{class.name}}, invalid format.", HttpStatus.BAD_REQUEST);
        }
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    @DeleteMapping("/{% raw %}{{% endraw %}{{class.properties[0].name}}{% raw %}}{% endraw %}/delete")
    public ResponseEntity<Object> delete(@PathVariable {{class.properties[0].type}} {{class.properties[0].name}}) {
        var deleted = {{class.name.lower()}}Service.delete({{class.properties[0].name}});

        if(deleted) return new ResponseEntity<>("{{class.name}} deleted", HttpStatus.OK);
        else return new ResponseEntity<>("{{class.name}} not found", HttpStatus.NOT_FOUND);
    }
}"""
