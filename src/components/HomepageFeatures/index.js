import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Easy to Use',
    icon: '🚀',
    description: (
      <>
        KaleidoSwap is an open-source desktop application designed for seamless 
        management of your RGB Lightning Node. Run your own node or connect to 
        existing ones with just a few clicks.
      </>
    ),
  },
  {
    title: 'RGB Asset Support',
    icon: '🎨',
    description: (
      <>
        Connect to RGB Lightning Service Providers (LSPs) to access liquidity and 
        trade RGB assets on the Lightning Network. Full support for RGB20.
      </>
    ),
  },
  {
    title: 'Lightning Fast',
    icon: '⚡',
    description: (
      <>
        Experience instant, low-cost RGB asset transfers powered by the Lightning 
        Network. Open channels, manage liquidity, and execute atomic swaps with 
        built-in security.
      </>
    ),
  },
];

function Feature({title, description, icon}) {
  return (
    <div className={clsx('col col--4')}>
      <div className={styles.featureCard}>
        <div className={styles.featureIcon}>{icon}</div>
        <h3 className={styles.featureTitle}>{title}</h3>
        <p className={styles.featureDescription}>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
} 