%% Load Images
fmri_nii = nifti('fmri/filtered_func_data_tempfilt_m24_wmcsf_drift.nii');
% nifti는 괄호 뒤 경로속 nii파일을 불러오는 함수이다. 이 코드파일을 fmri의 상위폴더에 두었기 때문에 fmri/를 넣는다.
fmri = double(fmri_nii.dat);
% fmri_nii데이터를 컴퓨터가 취급할 수 있는 0과 1 자릿수의 2배 자릿수를 취급하는 배정밀도로 전환해준다.
% 이 배정밀도는 유효 자릿수를 늘려 수치의 정밀도를 높여준다.
atlas_nii = nifti('fmri/aal2example_func.nii');
% nifti로 aal2example_func라는 nii파일을 불러온다. 마찬가지로 코드파일을 fmri의 상위폴더에 두어 fmri/를
% 넣어주었다.
atlas = double(atlas_nii.dat);
% 마찬가지로 atlass_nii 데이터를 배정밀도로 전환해준다. 그리고 이를 atlas라는 변수에 넣어주었다.
roi = load('aal90_values.txt');
% aal90_values라는 txt파일을 load 함수로 불러와준다. roi라는 변수에 넣어준다.
% 이 코드파일과 동일한 폴더에 두었기때문에 특별한 경로설정없이 바로 불러온다.

%% Compute average BOLD signals
n_time = size(fmri,4);
% fmri의 4번째 차원 길이를 불러온다. fmri는 4차원이고, 4번째 차원의 길이를 n_time이라고 설정하였다.
% size(fmri)는 [128,128,35,97]이 되고 이 중 네번째 차원이므로 97이 된다. 이는 output에서 확인할 수
% 있었다
n_region = length(roi);
% roi는 aal90_values.txt로 2001 ~ 8302까지 90개가 있었으므로 90이 된다.
ts = zeros(n_time,n_region);
% ts는 이후 결과값을 넣을 zero padding값이라고 보면된다. n_time * n_region tensor를 0으로 채운것이다
% 여기선 97*90 tensor가 전부 0으로 채워져있게 되는 것이다.
for i = 1:n_region
    % for 문으로 i라는 변수를 1부터 n_region까지 반복해준다. 여기선 i를 1부터 90까지 반복해주게 된다.
    idx = bsxfun(@plus, 0:numel(atlas):numel(fmri)-numel(atlas), find(atlas==roi(i)));
    % bsxfun(@plus,A,B)에서 플러스 연산을 배열 A와 배열 B에 적용하는 것이다.
    % numel은 행렬에 포함된 요소개수를 찾는다. numel(atlas)는 
    % 0부터 numel(fmri)-numel(atlas)까지 numel(atlas)의 단위로 뛰어서 (start:step:end)
    % roi(i)의 2001~8302까지의 숫자를 순서대로 atlas에 대입하여 그에 맞는 atlas를 찾는다.(i=1이면
    % 2001인 atlas). 같다는 연산자는 =을 두번써서 ==로 해주어야한다. -> find로 벡터값이 나온다.
    % 둘다 행이 1이고 열이 같은 행벡터 1*t값으로 나오게되고, 두개의 요소를 더하는것이 bsxfun이고 이렇게 더한 값을
    % idx라는 변수 안에 넣어주었다. find(atlas,,)는 열벡터 t2*1이 나와서 둘을 더하는 bsxfun을 해주면 
    % 행렬 배열이 나오게 된다.
    ts(:,i) = mean(fmri(idx),1)';
    % 97*90 zero padding tensor인 행렬 ts에 i번째 열에 fmri(idx) 요소의 평균값이 포함된 행벡터를
    % 반환한다. 97*1 열벡터를 i번째 열에 넣어주는 것이다. 이것이 90번 반복되므로 97*90에 값들이
    % fmri(idx)요소값 평균이 전부 들어가는 것이다.
end

%% Functional connectivity based on correlation
fc_correlation = corr(ts);
% 열벡터들의 상관관계를 구하는 것이다.
% functional connectivity를 구하기 위해 사용하는 방법 중 Cross-correlation방법을 이용한다.
% cross correlation은 두가지 region에 대해서 time delay를 추가해주어 time을 맞추어 비교하는 방법이다.
%% Functional connectivity based on coherence
% Cross correlation에서 frequency로 계산해주는 Cross-coherence 방법을 사용한다.
fc_coherence = zeros(n_region, n_region);
% n_region * n_region tensor를 모두 0으로 채운 것이다. ts와 똑같은 zero padding 값이다.
for i = 1:90
    % i를 1부터 90까지 for문을 돌린다.
    for j = i+1:90
        Cxy = mscohere(ts(:,i), ts(:,j), [], [], 128, 1/3);
        % roi들의 coherence를 구하는 함수가 mscohere이다. 레포트 작성
        % ts(:,i), ts(:,j)는 입력신호로 행렬값이다 (i,n번째 열)
        % 뒤에 [], []는 지정해주는 행렬을 위한 빈칸 배열이다.
        % 주파수는 128으로 Hz이다.f에 지정된 주파수에서의 크기 제곱 일관성 추정값을 반환
        % 1/3은 단위시간당 샘플 개수이다.
        fc_coherence(i,j) = mean(Cxy);
        % fc_coherence의 i행 j열의 값들의 평균값이 포함된 행벡터를 반환한다.
    end
end
fc_coherence = fc_coherence + fc_coherence' + eye(n_region);
% fc_coherence에다가 전치값(Transpose)인 fc_coherence'을 더한다 eye는 주 대각선이 1 (m*n에서 m=n) 
% 이고 나머지 요소가 0으로 구성된 n*n 크기의 단위 행렬을 반환한다. fc_coherence와 fc_coherence'는
% ROI끼리 더해주고 비교해준 것으로 나머지가 동일하다. 그래서 주대각선 i의 값과 전치된 두가지 값들이 모두
% 더해져 주 대각선이 3으로 같아지기 때문에 i가아니라 i+1를 넣어주어야 하는 것이다. 이을 통해 주 대각선이 
% 모두 1이 된다.


%% Plot
close all;
% 핸들이 숨겨지지 않은 모든 Figure를 삭제한다.
figure('Color', 'w');
% 'Color'를 흰색으로 이용하는 배경을 만든다.
subplot(1,2,1);
% Figure를 1*2 그리드로 나누고, 1의 위치에 좌표축을 만든다.(첫번째)
imagesc(fc_correlation);
% fc_correlation 데이터 전체를 이미지로 표시한다
% 결과 이미지는 1*2 그리드 픽셀이 나온다.
axis equal off;
% axis equal은 각 축에서의 데이터를 단위에 대해 동일한 길이를 사용하는 것, 축을 표시하지 않는다.
title('FC based on correlation');
% 이름을 FC based on correlation으로 짓는다.
subplot(1,2,2);
% Figure를 1*2 그리드로 나누고, 2의 위치에 좌표축을 만든다.(두번째)
imagesc(fc_coherence);
% fc_coherence 데이터 전체를 이미지로 표시한다
% 결과 이미지는 1*2 그리드 픽셀이 나온다.
axis equal off;
% 각 축에서의 데이터를 단위에 대해 동일한 길이를 사용하고, 축을 표시하지 않는다.
title('FC based on coherence');
% 이름을 FC based on coherence으로 짓는다.