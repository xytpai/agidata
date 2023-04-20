DST=$1

read -p "Are you sure to migrate? (Y/N):" para
case $para in
[yY])

smalldataset=(LCCC squad20 qingyun hc3-chinese glm-chinese colossalchat math_qa)
for item in ${smalldataset[*]}; do
CURDIR=${item}
OUTDIR=${DST}/${CURDIR}
echo "${CURDIR} -> ${OUTDIR}"
mkdir -p ${OUTDIR}
cp ${CURDIR}/*.py ${OUTDIR} 2>/dev/null
cp ${CURDIR}/*.json ${OUTDIR} 2>/dev/null
cp ${CURDIR}/*.jsonl ${OUTDIR} 2>/dev/null
cp ${CURDIR}/*.parquet ${OUTDIR} 2>/dev/null
cp ${CURDIR}/*.zip ${OUTDIR} 2>/dev/null
cp ${CURDIR}/*.csv ${OUTDIR} 2>/dev/null
cp ${CURDIR}/*.tar ${OUTDIR} 2>/dev/null
cd ${OUTDIR}
python check.py
cd -
done

mediumdataset=(chinese_chatgpt_corpus belle wiki_zh baike web_qa)
for item in ${mediumdataset[*]}; do
CURDIR=${item}
OUTDIR=${DST}/${CURDIR}
echo "${CURDIR} -> ${OUTDIR}"
mkdir -p ${OUTDIR}
cp ${CURDIR}/*.py ${OUTDIR} 2>/dev/null
cp ${CURDIR}/*.json ${OUTDIR} 2>/dev/null
cp ${CURDIR}/*.jsonl ${OUTDIR} 2>/dev/null
cp ${CURDIR}/*.parquet ${OUTDIR} 2>/dev/null
cp ${CURDIR}/*.zip ${OUTDIR} 2>/dev/null
cp ${CURDIR}/*.csv ${OUTDIR} 2>/dev/null
cp ${CURDIR}/*.tar ${OUTDIR} 2>/dev/null
cd ${OUTDIR}
python check.py
cd -
done

;;
*)
exit 1
;;
esac
