import styles from './Vacancy.module.css'

export function Vacancy({name, text, experience, company, city}) {
    return (
        <div>
            <div className={styles.card}>
                <h2 className={styles.title}>{name}</h2>
                <p className={styles.salary}>{text}</p>
                <p className={styles.experience}>{experience}</p>
                <p className={styles.company}>{company}</p>
                <p className={styles.location}>{city}</p>
            </div>
        </div>
    )
}