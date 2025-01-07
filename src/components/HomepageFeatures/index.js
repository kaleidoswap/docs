import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Easy to Use',
    icon: '🚀',
    description: (
      <>
        KaleidoSwap was designed to be easily integrated into your applications
        with comprehensive documentation.
      </>
    ),
  },
  {
    title: 'RGB Asset Support',
    icon: '🎨',
    description: (
      <>
        Trade RGB assets securely and efficiently using our decentralized protocol.
      </>
    ),
  },
  {
    title: 'Lightning Fast',
    icon: '⚡',
    description: (
      <>
        Built on Lightning Network for instant, low-cost transactions.
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