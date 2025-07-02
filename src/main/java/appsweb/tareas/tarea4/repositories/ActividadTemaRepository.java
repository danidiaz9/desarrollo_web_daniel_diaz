package appsweb.tareas.tarea4.repositories;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import appsweb.tareas.tarea4.models.ActividadTema;

public interface ActividadTemaRepository extends JpaRepository<ActividadTema, Integer> {
    List<ActividadTema> findByActividadId(Integer actividadId); 
}
