import React, { useState } from 'react';
import styles from '@/app/styles/sideBar.module.css';
import { BRANDS } from '@/app/components/sidebar/modeldata'; // 새로 생성한 파일에서 BRANDS를 가져옵니다.
import { useBrandStore } from '@/app/store/brandStore';


export function ModelSelectContainer() {
    const {
      selectedBrand, selectedModel,
      setSelectedBrand, setSelectedModel, } = useBrandStore();

    const handleBrandChange = (brandId: string) => {
        setSelectedBrand(brandId);
        setSelectedModel(''); // 브랜드 변경 시 모델 선택 초기화
    };

    const handleModelChange = (modelId: string) => {
        setSelectedModel(modelId);
    };

    const handleReset = () => {
      setSelectedBrand('');
      setSelectedModel('');
    }

    const selectedBrandData = BRANDS.find(brand => brand.id === selectedBrand);

  return (
    <div className={styles.container}>
      <div className={styles.headerRow}> 
        <h2 className={styles.containerTitle}>카메라 모델 선택</h2>
        <button onClick={handleReset} className={styles.resetButton} title="초기화">
            ⟳
        </button>
      </div>
      <div className={styles.selectGroup}>
        <div className={styles.selectRow}>
          <label className={styles.selectLabel}>브랜드</label>
          <select
            className={styles.modelSelect}
            value={selectedBrand || ''}
            onChange={(e) => handleBrandChange(e.target.value)}
          >
            <option value="">브랜드를 선택하세요</option>
            {BRANDS.map((brand) => (
              <option key={brand.id} value={brand.id}>
                {brand.name}
              </option>
            ))}
          </select>
        </div>

        {selectedBrand && (
          <div className={styles.selectRow}>
            <label className={styles.selectLabel}>모델</label>
            <select
              className={styles.modelSelect}
              value={selectedModel || ''}
              onChange={(e) => handleModelChange(e.target.value)}
            >
              <option value="">모델을 선택하세요</option>
              {selectedBrandData?.models.map((model) => (
                <option key={model.id} value={model.id}>
                  {model.name}
                </option>
              ))}
            </select>
          </div>
        )}

        {selectedBrand && selectedModel && (
          <div className={styles.selectedInfo}>
            선택된 모델: {selectedBrandData?.models.find(m => m.id === selectedModel)?.name}
          </div>
        )}
        
      </div>
    </div>
  );
}