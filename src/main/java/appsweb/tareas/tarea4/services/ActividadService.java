package appsweb.tareas.tarea4.services;

import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.time.LocalDateTime;

import org.springframework.stereotype.Service;

import appsweb.tareas.tarea4.repositories.ActividadRepository;
import appsweb.tareas.tarea4.repositories.NotaRepository;
import appsweb.tareas.tarea4.models.Actividad;
import appsweb.tareas.tarea4.models.Nota;

@Service
public class ActividadService {
    private final ActividadRepository actividadRepository;
    private final NotaRepository notaRepository;

    public ActividadService(ActividadRepository actividadRepository, NotaRepository notaRepository) {
        this.actividadRepository = actividadRepository;
        this.notaRepository = notaRepository;
    }

    public List<Actividad> getCompletedActivities() {
        return actividadRepository.findByDiaHoraTerminoBefore(LocalDateTime.now());
    }

    public Map<Actividad, Double> getCompletedActivitiesWithPromedio() {
        List<Actividad> actividades = getCompletedActivities();
        Map<Actividad, Double> resultado = new HashMap<>();
        for (Actividad act : actividades) {
            List<Nota> notas = notaRepository.findByActividadId(act.getId());
            Double promedio = null;
            if (notas != null && !notas.isEmpty()) {
                promedio = notas.stream().mapToInt(Nota::getNota).average().orElse(0.0);
            }
            resultado.put(act, promedio);
        }
        return resultado;
    }

    public void agregarNotaActividad(Integer actividadId, Integer valor) {
        Actividad actividad = actividadRepository.findById(actividadId)
                .orElseThrow(() -> new IllegalArgumentException("Actividad no encontrada"));
        if (valor == null || valor < 1 || valor > 7) {
            throw new IllegalArgumentException("La nota debe estar entre 1 y 7");
        }
        Nota nota = new Nota();
        nota.setNota(valor);
        nota.setActividad(actividad);
        notaRepository.save(nota);
    }
}
