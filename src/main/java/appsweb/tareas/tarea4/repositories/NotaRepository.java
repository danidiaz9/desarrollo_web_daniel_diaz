package appsweb.tareas.tarea4.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import appsweb.tareas.tarea4.models.Nota;

import java.util.List;

@Repository
public interface NotaRepository extends JpaRepository<Nota, Integer> {
    List<Nota> findByActividadId(Integer actividadId);
}
