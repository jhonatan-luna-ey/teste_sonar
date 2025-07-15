```java
import java.util.Calendar;
import java.util.logging.Logger;

public class ExemploSonarQube {

    private static final Logger logger = Logger.getLogger(ExemploSonarQube.class.getName());

    public static void main(String[] args) {
        // Criando um objeto da classe Date
        Calendar calendar = Calendar.getInstance();
        calendar.set(2023, Calendar.JANUARY, 1);
        java.util.Date data = calendar.getTime();

        // Exibindo a data
        logger.info("A data é: " + data);
    }
}
```