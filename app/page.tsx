export default function Home() {
  return (
    <main style={{
      minHeight: '100vh',
      background: '#0A0A0A',
      color: '#F5F0E8',
      fontFamily: 'var(--font-inter), sans-serif',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      <div style={{
        maxWidth: '700px',
        textAlign: 'center',
        padding: '3rem',
      }}>
        <h1 style={{
          fontFamily: 'var(--font-cormorant), serif',
          fontSize: '3.5rem',
          color: '#C9A961',
          marginBottom: '1rem',
          fontWeight: 300,
        }}>AMARIGOM DECO</h1>
        <p style={{
          fontSize: '1.2rem',
          color: '#A0998C',
          marginBottom: '3rem',
          lineHeight: 1.6,
        }}>Cortinas Roller Blackout, Sunscreen y Tradicionales</p>

        <div style={{
          background: '#1A1A1A',
          border: '1px solid #2A2520',
          borderRadius: '12px',
          padding: '2.5rem',
          textAlign: 'left',
        }}>
          <h2 style={{
            color: '#C9A961',
            fontFamily: 'var(--font-cormorant), serif',
            fontSize: '1.5rem',
            marginBottom: '1.5rem',
            fontWeight: 400,
          }}>Proyecto Flask</h2>
          <p style={{ color: '#A0998C', lineHeight: 1.8, marginBottom: '1.5rem' }}>
            Este proyecto esta desarrollado con Python Flask. Para ejecutarlo en tu computadora:
          </p>
          <div style={{
            background: '#0A0A0A',
            borderRadius: '8px',
            padding: '1.5rem',
            fontFamily: 'var(--font-inter), monospace',
            fontSize: '0.9rem',
            lineHeight: 2,
            color: '#C9A961',
          }}>
            <div><span style={{color:'#A0998C'}}>1.</span> pip install -r requirements.txt</div>
            <div><span style={{color:'#A0998C'}}>2.</span> {'Crear archivo .env con las variables'}</div>
            <div><span style={{color:'#A0998C'}}>3.</span> python app.py</div>
            <div><span style={{color:'#A0998C'}}>4.</span> {'Abrir http://localhost:5000'}</div>
          </div>
          <p style={{ color: '#6B6560', marginTop: '1.5rem', fontSize: '0.85rem' }}>
            Descarga el proyecto con el boton de los tres puntos {'>'} Download ZIP
          </p>
        </div>
      </div>
    </main>
  )
}
