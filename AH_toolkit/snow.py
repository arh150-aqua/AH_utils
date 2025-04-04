'''
script to extract queue data (s3 images path/annotation information) as parquets from snowflake 
IMPORTANT: Need To Modify [queue_name] Variable
'''

import pandas as pd
from snowbyte import snowflake_query_to_df
from functools import partial
from collections import defaultdict



def flatten_annotations(df):
    anns=defaultdict(list)
    for i, r in df.iterrows():
        if r.annotation:
            ann = r.annotation
            if "annotations" not in ann:
                continue
        else:
            continue

        for a in ann["annotations"]:
            anns["image_url"].append(r.image_urls[0]    )
            anns["annotator_email"].append(r.annotator_email)
            anns["label"].append(a.get("label", None))
            anns["category"].append(a.get("category", None))
            anns["height"].append(a.get("height", None))
            anns["width"].append(a.get("width", None))
            anns["xCrop"].append(a.get("xCrop", None))
            anns["yCrop"].append(a.get("yCrop", None))
            anns["workflow_name"].append(r.workflow_name)
            anns["plali_annotation_id"].append(r.plali_annotation_id)
            anns["plali_image_id"].append(r.plali_image_id)
            anns["skipped"].append(False)
            anns["duration"].append(pd.Timedelta(r.duration).total_seconds())
            anns["annotation_time"].append(r.annotation_time)

    return pd.DataFrame(anns)


def get_snow_queues(queue_names, ssm_name = "/dsn/snowflake/anthony"):

    snowflake_query = partial(snowflake_query_to_df, ssm_name=ssm_name)

    sql=f"""   
                    select
                        pw.id as pw_id
                        , pw.name as workflow_name
                        , pi.id as pi_id
                        , pi.metadata
                        , pi.images as image_urls
                        , pa.id as pa_id
                        , pa.annotation
                        , pa.annotator_email
                        , pa.plali_image_id
                        , pa.id as plali_annotation_id
                        , pa.annotation_time as annotation_time
                        , pa.duration as duration

                    from     prod.plali_workflows as pw
                        join prod.plali_images as pi on pi.workflow_id = pw.id
                        join prod.plali_annotations as pa on pa.plali_image_id = pi.id

                    where workflow_name in {queue_names};
                """
    df = snowflake_query(sql, json_cols=["image_urls", "annotation"])

    anns=flatten_annotations(df)
    
    info = {} 
    for label, label_df in anns.groupby('label'):
        info[label] = f"Num annotations {len(label_df)}"

    return df, anns, info


# queue_names="""('pellet_bbox_aquanvr_feeding_cam_2025-03-01_2025-03-15_q1')"""
# df, anns, info = get_snow_queues(queue_names)