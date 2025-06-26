import os.path
import datetime
import cv2
import numpy as np
import torch
import pickle

import matplotlib.pyplot as plt

def test_pytorch_loader(model, test_input_handle, configs, itr):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') , 'test...')
    res_path = os.path.join(configs.gen_frm_dir, str(itr))
    os.mkdir(res_path)

    for batch_id, test_ims in enumerate(test_input_handle):

        # Support for annotation mask
        has_ann_mask = False
        if isinstance(test_ims, dict) and 'annotation_mask' in test_ims:
            ann_mask = test_ims['annotation_mask'].numpy()
            has_ann_mask = True
        else:
            ann_mask = None

        test_ims = test_ims['radar_frames'].numpy()
        img_gen = model.test(test_ims)
        output_length = configs.total_length - configs.input_length

        def save_plots(field, labels, res_path, figsize=None,
                       vmin=0, vmax=10, cmap="viridis", npy=False, **imshow_args):

            for i, data in enumerate(field):
                fig = plt.figure(figsize=figsize)
                ax = plt.axes()
                ax.set_axis_off()
                alpha = data[..., 0] / 1
                alpha[alpha < 1] = 0
                alpha[alpha > 1] = 1

                img = ax.imshow(data[..., 0], alpha=alpha, vmin=vmin, vmax=vmax, cmap=cmap, **imshow_args)
                plt.savefig('{}/{}.png'.format(res_path, labels[i]))
                plt.close()  
                if npy:
                    with open( '{}/{}.npy'.format(res_path, labels[i]), 'wb') as f:
                        np.save(f, data[..., 0])


        data_vis_dict = {
            'radar': {'vmin': 1, 'vmax': 40},
        }
        vis_info = data_vis_dict[configs.dataset_name]

        if batch_id <= configs.num_save_samples:
            path = os.path.join(res_path, str(batch_id))
            os.mkdir(path)
            if configs.case_type == 'normal':
                test_ims_plot = test_ims[0][:-2, 256-192:256+192, 256-192:256+192]
                img_gen_plot = img_gen[0][:-2, 256-192:256+192, 256-192:256+192]
            else:
                test_ims_plot = test_ims[0][:-2]
                img_gen_plot = img_gen[0][:-2]
            save_plots(test_ims_plot,
                       labels=['gt{}'.format(i + 1) for i in range(configs.total_length)],
                       res_path=path, vmin=vis_info['vmin'], vmax=vis_info['vmax'])
            save_plots(img_gen_plot,
                       labels=['pd{}'.format(i + 1) for i in range(9, configs.total_length)],
                       res_path=path, vmin=vis_info['vmin'], vmax=vis_info['vmax'])

            # --- Visualization: ground truth, prediction, annotation mask ---
            if has_ann_mask:
                gt_img = test_ims_plot[0][..., 0]  # First channel only
                pred_img = img_gen_plot[0][..., 0]  # First channel only
                # Ensure annotation mask is 2D
                if ann_mask.ndim == 3:
                    ann_mask = ann_mask[..., 0]
                ann_img = ann_mask
                if ann_img.shape != gt_img.shape:
                    ann_img = cv2.resize(ann_img, (gt_img.shape[1], gt_img.shape[0]))
                fig, axs = plt.subplots(1, 3, figsize=(12, 4))
                axs[0].imshow(gt_img, cmap='viridis')
                axs[0].set_title('Ground Truth')
                axs[1].imshow(pred_img, cmap='viridis')
                axs[1].set_title('Prediction')
                axs[2].imshow(ann_img, cmap='gray')
                axs[2].set_title('Annotation Mask')
                for ax in axs:
                    ax.axis('off')
                plt.tight_layout()
                # Save PNG
                plt.savefig(os.path.join(path, 'compare_gt_pred_ann.png'))
                # Show interactively
                plt.show()
                plt.close()

    print('finished!')